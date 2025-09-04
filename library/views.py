from rest_framework import viewsets
from library.models import Author, Book, Member,BorrowRecord
from library.serializers import AuthorSerializer, BookSerializer, MemberSerializer,BorrowRecordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.http import HttpResponse


from django.http import HttpResponse


def home(request):
    html = """
    <h2>Welcome to Booktopia!</h2>
    <p>Available endpoints:</p>
    <ul>
        <li><a href="/api/books/">/api/books/</a>  CRUD for books</li>
        <li><a href="/api/authors/">/api/authors/</a> CRUD for authors</li>
        <li><a href="/api/members/">/api/members/</a>  CRUD for members</li>
        <li><a href="/api/borrow/">/api/borrow/</a>  Borrow a book</li>
        <li><a href="/api/return/">/api/return/</a> Return a book</li>
    </ul>
    """
    return HttpResponse(html, content_type="text/html")

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):   # make sure it's ModelViewSet
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class MemberViewSet(viewsets.ModelViewSet):   # also ModelViewSet
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class BorrowView(APIView):

    def post(self,request):

        book_id = request.data.get('book_id')
        member_id = request.data.get('member_id')

        if not book_id or not member_id:
            return Response({"detail":"book_id and member_id required"},status=status.HTTP_404_NOT_FOUND)
        
        book = Book.objects.select_for_update().filter(pk =book_id).first()

        if not book:
            return Response({"detail": "Invalid book_id"}, status=status.HTTP_404_NOT_FOUND)
        
        if not book.is_available:
            return Response({"detail": "Book not available"}, status=status.HTTP_400_BAD_REQUEST)
        

        member = Member.objects.filter(pk=member_id).first()
        if not member:
            return Response({"detail": "Invalid member_id"}, status=status.HTTP_404_NOT_FOUND)

        record = BorrowRecord.objects.create(book=book, member=member)
        book.is_available = False
        book.save(update_fields=["is_available"])

        return Response(BorrowRecordSerializer(record).data, status=status.HTTP_201_CREATED)
    
class ReturnView(APIView):

    def post(self,request):

        book_id = request.data.get('book_id')

        book = Book.objects.select_for_update().filter(pk=book_id).first()
        if not book_id:
            return Response({"detail":"book_id required."},status=status.HTTP_400_BAD_REQUEST)
        
        record = BorrowRecord.objects.filter(book=book, return_date__isnull=True).first()
        if not record:
            return Response({"detail":"No active borrow record found."},status=status.HTTP_404_NOT_FOUND)
        
        record.return_date = timezone.now()
        record.save(update_fields=["is_available"])

        return Response(BorrowRecordSerializer(record).data,status=status.HTTP_200_OK)

        

