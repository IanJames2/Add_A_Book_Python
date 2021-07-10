from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index),
    path('registration', views.Registration),
    path('favorite_books_input', views.Login),
    path('books', views.User_Logged_In),
    path('user_leaves', views.logout),
    path('added_book_to_site/', views.Add_Book_To_Site),
    path('books/edit_tag', views.Edit_FavBook),
    path('books/<int:bookid>', views.Details_Read),
    path('<int:bookid>/delete', views.delete_atag),
    path('<int:bookid>', views.update_book),
    path('favbooks/<int:bookid>', views.add_to_fav_book_list),
    path('remove_favbooks/<int:bookid>', views.remove_from_book_list),
    path('books/goback', views.back)
    # path('add_book_to_fav_list/<int:bookid>', views.add_book_to_fav_list)
]
