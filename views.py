from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import Book, Cart, Wishlist, Order




# HOME PAGE

def home(request):

    search = request.GET.get('search')

    if search:
        books = Book.objects.filter(title__icontains=search)
    else:
        books = Book.objects.all()

    context = {
        'books': books
    }

    return render(request, 'store/home.html', context)


# BOOK DETAIL PAGE

def book_detail(request, id):

    book = get_object_or_404(Book, id=id)

    context = {
        'book': book
    }

    return render(request, 'store/book_detail.html', context)


# SEARCH BOOKS

def search_books(request):

    query = request.GET.get('search')

    books = []

    if query:
        books = Book.objects.filter(title__icontains=query)

    context = {
        'books': books
    }

    return render(request, 'store/search.html', context)


# ADD TO CART

@login_required
def add_to_cart(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        book=book
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# VIEW CART

@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.book.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total': total
    }

    return render(request, 'store/cart.html', context)


# REMOVE FROM CART

@login_required
def remove_from_cart(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart')


# ADD TO WISHLIST

@login_required
def add_to_wishlist(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        book=book
    )

    return redirect('wishlist')


# VIEW WISHLIST

@login_required
def wishlist(request):

    items = Wishlist.objects.filter(user=request.user)

    context = {
        'items': items
    }

    return render(request, 'store/wishlist.html', context)


# REMOVE FROM WISHLIST

@login_required
def remove_wishlist(request, item_id):

    item = get_object_or_404(
        Wishlist,
        id=item_id,
        user=request.user
    )

    item.delete()

    return redirect('wishlist')



# LOGIN USER

def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect('/')

    return render(request, 'store/login.html')


# LOGOUT USER

def logout_view(request):

    logout(request)

    return redirect('/')


# CHECKOUT

@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.book.price * item.quantity

    Order.objects.create(
        user=request.user,
        total_price=total
    )

    cart_items.delete()

    return render(request, 'store/checkout_success.html')


from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


from django.shortcuts import get_object_or_404, redirect
from .models import Book


def generate_summary(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    # IKIGAI
    if book.title.lower() == "ikigai":

        summary = """
        Ikigai explores the Japanese philosophy of finding purpose and happiness in everyday life.
        The book explains how passion, mission, vocation, and profession come together to create
        a meaningful life. Through practical wisdom, healthy lifestyle habits, and inspiring stories
        from Japanese culture, the book encourages readers to live with balance, mindfulness,
        and long-term fulfillment.
        """

    # THE ALCHEMIST
    elif book.title.lower() == "the alchemist":

        summary = """
        The Alchemist follows the journey of Santiago, a young shepherd boy who dreams of discovering
        treasure in Egypt. Along his journey, he learns valuable lessons about destiny, courage, love,
        and listening to one’s heart. The novel inspires readers to pursue their dreams and trust
        the journey of life, showing that true treasure often lies within personal growth and self-discovery.
        """

    # THE PRAGMATIC PROGRAMMER
    elif book.title.lower() == "the pragmatic programmer":

        summary = """
        The Pragmatic Programmer is a classic software development book that teaches practical approaches
        to becoming a better programmer. It covers problem-solving, coding practices, debugging,
        teamwork, and continuous learning. The book encourages developers to write clean,
        maintainable code and adapt to changing technologies while improving both technical
        and professional skills.
        """

    # HARRY POTTER
    elif book.title.lower() == "harry potter and the sorcerer's stone":

        summary = """
        Harry Potter and the Sorcerer’s Stone tells the magical story of Harry Potter,
        a young boy who discovers that he is a wizard. He joins Hogwarts School of Witchcraft
        and Wizardry, where he makes friends, learns magic, and uncovers secrets about his past.
        Filled with adventure, friendship, and mystery, the story introduces readers to a magical
        world loved by millions around the globe.
        """

    # CLEAN CODE
    elif book.title.lower() == "clean code":

        summary = """
        Clean Code focuses on writing readable, maintainable, and efficient software code.
        The book teaches developers how to improve coding standards, naming conventions,
        functions, testing, and overall software design. It emphasizes simplicity and clarity,
        helping programmers build professional-quality applications that are easier to understand
        and maintain over time.
        """

    # THINK AND GROW RICH
    elif book.title.lower() == "think and grow rich":

        summary = """
        Think and Grow Rich explores the mindset and habits needed for achieving financial success
        and personal growth. Based on lessons from successful individuals, the book discusses desire,
        persistence, self-confidence, goal setting, and positive thinking. It motivates readers to
        develop discipline and a success-oriented mindset to achieve their dreams and ambitions.
        """

    # DEFAULT SUMMARY
    else:

        summary = f"""
        {book.title} by {book.author} is an engaging book in the {book.category} category.

        This book explores important themes, interesting characters, and valuable insights
        that keep readers interested throughout the journey.

        Readers who enjoy {book.category} books will find this title informative,
        entertaining, and inspiring.

        Highly recommended for book lovers looking for a meaningful reading experience.
        """

    # SAVE SUMMARY
    book.summary = summary
    book.save()

    return redirect('book_detail', id=book.id)
from django.shortcuts import render, get_object_or_404
from .models import Book, Category


def category_books(request, id):

    category = get_object_or_404(Category, id=id)

    books = Book.objects.filter(category=category)

    context = {
        'category': category,
        'books': books
    }

    return render(request, 'store/category_books.html', context)


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(request, 'Invalid Username or Password')

    return render(request, 'store/login.html')


def user_logout(request):

    logout(request)

    return redirect('home')

from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def admin_dashboard(request):

    return render(request, 'store/admin_dashboard.html')


from django.contrib import messages



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# REGISTER VIEW
def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check existing username
        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(request, "Account created successfully")

        return redirect('login')

    return render(request, 'store/register.html')


# LOGIN VIEW
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # ADMIN LOGIN
            if user.is_superuser:
                login(request, user)
                return redirect('/admin/')

            # NORMAL USER LOGIN
            else:
                login(request, user)
                return redirect('/')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'store/login.html')


# LOGOUT VIEW
def logout_view(request):

    logout(request)

    return redirect('/')


from django.contrib import messages
from django.shortcuts import redirect


def subscribe(request):

    if request.method == 'POST':

        email = request.POST.get('email')

        messages.success(
            request,
            "Thank you for subscribing to our bookstore newsletter!"
        )

    return redirect('/')