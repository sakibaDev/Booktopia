from rest_framework import serializers
from library.models import Author,Book,Member,BorrowRecord

class AuthorSerializer(serializers.Serializer):

    class Meta:
        model = Author
        fields =['id','name','biography']

class BookSerializer(serializers.Serializer):

    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields =['id','title','author','isbn','category','is_available']

class MemberSerializer(serializers.Serializer):

    class Meta:
        model = Member
        fields =['id','name','email','membership_date']

class BorrowRecordSerializer(serializers.Serializer):

    book = serializers.PrimaryKeyRelatedField(queryset = Book.objects.all())
    member = serializers.PrimaryKeyRelatedField(queryset = Member.objects.all())

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'member', 'borrow_date', 'return_date']
        read_only_fields = ['borrow_date', 'return_date']