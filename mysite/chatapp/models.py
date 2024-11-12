from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings




class ChatRoom(models.Model):
    """
    Represents a chat room where users can exchange messages.
    
    Attributes:
        name (str): The display name of the chat room
        slug (str): URL-friendly unique identifier
        created_by (User): Reference to the user who created the room
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def save(self, *args, **kwargs):
        """
        Override save method to create a system message when a new room is created.
        
        Creates an automatic ChatMessage to record room creation if this is a new room
        and has a creator assigned.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.created_by:
            ChatMessage.objects.create(
                user=self.created_by,
                room=self,
                message_content=f"{self.created_by.username} created this chatroom"
            )


class ChatMessage(models.Model):
    """
    Represents an encrypted message within a chat room.
    
    Messages are automatically encrypted when saved and decrypted when accessed
    through the decrypted_content property.
    
    Attributes:
        user (User): The user who sent the message
        room (ChatRoom): The chat room this message belongs to
        message_content (str): The encrypted message content
        date (datetime): Timestamp when the message was created
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    message_content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override save method to encrypt message content before saving.
        
        Encryption only occurs on new messages (not on updates) using the
        ENCRYPTION_KEY from settings.
        """
        # Encrypt message before saving
        if not self.pk:  # Only encrypt if it's a new message
            f = Fernet(settings.ENCRYPTION_KEY)
            self.message_content = f.encrypt(self.message_content.encode()).decode()
        super().save(*args, **kwargs)

    @property
    def decrypted_content(self):
        """
        Decrypt and return the message content.
        
        Returns:
            str: The decrypted message content, or an error message if decryption fails
        """
        # Decrypt message when accessed
        try:
            f = Fernet(settings.ENCRYPTION_KEY)
            return f.decrypt(self.message_content.encode()).decode()
        except Exception as e:
            return "Error decrypting message"

    class Meta:
        """Ensure messages are always ordered by date"""
        ordering = ('date',)