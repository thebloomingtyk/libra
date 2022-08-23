from django.contrib import admin

from catalog.models import Author, Book, BookInstance, Genre, Language

# Register your models here.

class BooksInline(admin.TabularInline):
    model = Book
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]



class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'due_back','borrower', 'id'] 
    list_filter = ('status', 'due_back')
    fieldsets = ((None, {
        'fields': ('book','imprint', 'id')
    }),
    ('Availability', {
        'fields': ('status', 'due_back', 'borrower')
    }),
)
    


admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Language)
admin.site.register(Genre)
admin.site.register(Author, AuthorAdmin)