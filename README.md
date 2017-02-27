# LearnDjango

#How to install Django

##Install Python

##Install Apache and mod_wsgi
**Django supports many other deployment options. One is uWSGI; it works very well with nginx**

##Get your database running

##Remove any old versions of Django

##Install the Django code
**Installing an official release with pip**
**Installing a distribution-specific package**
**Installing the development version**

#Models and databases

##Models
Fields
Field types
Field options
Automatic primary key fields
**If Django sees you’ve explicitly set Field.primary_key, it won’t add the automatic id column.**
Verbose field names
Relationships
ref SQL
**Custom field types**
Meta options
 **is “anything that’s not a field”**
 
 **Model methods**
 This is a valuable technique for keeping business logic in one place – the model
**Overriding predefined model methods**
It’s important to remember to call the superclass method
**Executing custom SQL**

Model inheritance
1. Abstract base classes 
put abstract=True in the Meta class.
Meta inheritance

part of the value should contain '%(app_label)s' and '%(class)s'.


2. Multi-table inheritance 
3. Proxy models

Multiple inheritance
use an explicit AutoField in the base models
use a common ancestor to hold the AutoField

Field name “hiding” is not permitted

Explicitly importing each model

##Making queries

###Creating objects
1. Django doesn’t hit the database until you explicitly call save().
2. To create and save an object in a single step, use the create() method

To add multiple records to a ManyToManyField in one go, include multiple arguments in the call to add(),

**Retrieving specific objects with filters**
**Chaining filters**

Lookups that span relationships

**Spanning multi-valued relationships**

1. Blog.objects.filter(entry__headline__contains='Lennon', entry__pub_date__year=2008)

2. Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008)

Filters can reference fields on the model

The pk lookup shortcut

Caching and QuerySets

**When QuerySets are not cached**

**Complex lookups with Q objects**

**Copying model instances**
more complicated if you use inheritance

Updating multiple objects at once

One-to-many relationships

Many-to-many relationships
plus '_set'

Falling back to raw SQL

##Aggregation
Generating aggregates over a QuerySet
1. Book.objects.all().aggregate(Avg('price'))
2. Book.objects.all().aggregate(Max('price'))

Generating aggregates for each item in a QuerySet

Combining multiple aggregations
Book.objects.annotate(Count('authors'), Count('store'))

Joins and aggregates
Store.objects.annotate(min_price=Min('books__price'), max_price=Max('books__price'))

Following relationships backwards

Aggregations and other QuerySet clauses


**values()**
An annotation is then provided for each unique group;

**Order** of annotate() and values() clauses
That's different

Interaction with default ordering or order_by()
class Meta:
        ordering = ["name"]

Aggregating annotations
For example, if you wanted to calculate the average number of authors per book you first annotate the set of books with the author count, then aggregate that author count, referencing the annotation field:
Book.objects.annotate(num_authors=Count('authors')).aggregate(Avg('num_authors'))


##Search

**Standard textual queries**
Author.objects.filter(name__contains='Terry')

**A database’s more advanced comparison functions**
1. If you’re using PostgreSQL, Django provides a selection of database specific tools
2. Other databases have different selections of tools

**Document-based search**
1. some of the most prominent are Elastic and Solr
2. PostgreSQL has its own full text search implementation built-in.



##Managers

Manager names

Custom managers
Adding extra manager methods
Modifying a manager’s initial QuerySet

**Default managers**
**Base managers**
Using managers for related object access
_Don’t filter away any results in this type of manager subclass_
_This manager is used to access objects that are related to from some other model_

Calling custom QuerySet methods from the manager

**Creating a manager with QuerySet methods**
Not every QuerySet method makes sense at the Manager level

**from_queryset()**
you might want both a custom Manager and a custom QuerySet

###Custom managers and model inheritance

**Implementation concerns**
Whatever features you add to your custom Manager, it must be possible to make a shallow copy of a Manager instance


##Performing raw SQL queries

###Performing raw queries
The raw() manager method can be used to perform raw SQL queries that return model instances
**Mapping query fields to model fields**
raw() automatically maps fields in the query to fields on the model
Alternatively, you can map fields in the query to model fields using the translations argument to raw().
**Index lookups**
raw() supports indexing
**Deferring model fields**
**Adding annotations**
You can also execute queries containing fields that aren’t defined on the model
**Passing parameters into raw()**
params is a list or dictionary of parameters

###Executing custom SQL directly
perform queries that don’t map cleanly to models
django.db.connection
**django.db.connections**
If you are using more than one database, you can use django.db.connections to obtain the connection (and cursor) for a specific database

1. fetchall()
((54360982, None), (54360880, None))
2. def dictfetchall(cursor)
[{'parent_id': None, 'id': 54360982}, {'parent_id': None, 'id': 54360880}]
3. def namedtuplefetchall(cursor)
[Result(id=54360982, parent_id=None), Result(id=54360880, parent_id=None)]

**Connections and cursors**
with connection.cursor() as c:
    c.execute(...)

##Database transactions
###Managing database transactions
**Django’s default transaction behavior**
autocommit mode
**Tying transactions to HTTP requests**
non_atomic_requests
It only works if it’s applied to the view itself.
**Controlling transactions explicitly**
1. decorator
@transaction.atomic
2. context manager
with transaction.atomic():
###Autocommit
Why Django uses autocommit
**Deactivating transaction management**
setting AUTOCOMMIT to False in its configuration
###Performing actions after commit
New in Django 1.9
Django provides the on_commit() function to register callback functions that should be executed after a transaction is successfully committed:
You can also wrap your function in a lambda
**Savepoints**
**Order of execution**
the order they were registered
**Exception handling**
**Timing of execution**
* two-phase commit
* commit functions only work with autocommit mode
**Use in tests**
TransactionTestCase Maybe need
**Why no rollback hook**
instead of doing something during the atomic block (transaction) and then undoing it if the transaction fails, 
use on_commit() to delay doing it in the first place until after the transaction succeeds

###Low-level APIs
* Django will refuse to turn autocommit off when an atomic() block is active, because that would break atomicity

* Django doesn’t provide an API to start a transaction. The expected way to start a transaction is to disable autocommit with set_autocommit().

* A savepoint is a marker within a transaction that enables you to roll back part of a transaction, rather than the full transaction

###Database-specific notes
* SQLite ≥ 3.6.8, hardly usable
* MySQL version and the table types(“InnoDB” or “MyISAM”.)
* PostgreSQL 
1. Transaction rollback
would be lost, even though that operation raised no error itself
2. Savepoint rollback
will not be undone in the case where b.save() raises an exception ╮(╯▽╰)╭

##Multiple databases
###Defining your databases
**Defining your databases**
settings.py
If the concept of a default database doesn’t make sense in the context of your project, 
you need to be careful to always specify the database that you want to use
**Synchronizing your databases**
 --database option, you can tell it to synchronize a different database
**Using other management commands**

###Automatic database routing
**Database routers**
1. db_for_read
2. db_for_write
3. allow_relation
4. allow_migrate
**Using routers**
1. First we want a router that knows to send queries
2. a router that sends all other apps to the
3. settings 
file DATABASE_ROUTERS = ['path.to.AuthRouter', 'path.to.PrimaryReplicaRouter']

###Manually selecting a database
priority higher than router
**Manually selecting a database for a QuerySet**
using() takes a single argument: the alias of the database
**Selecting a database for save()**
Moving an object from one database to another
two ways : 
1. Clear the primary key, Write a completely new object
2. force_insert option to save() 
**Selecting a database to delete from**
**Using managers with multiple databases**
Using get_queryset() with multiple databases
_db attribute on the manager

###Exposing multiple databases in Django’s admin interface
Django’s admin doesn’t have any explicit support for multiple databases
need to write custom ModelAdmin classes
five methods that require customization


###Using raw cursors with multiple databases
cursor = connections['my_db_alias'].cursor()

###Limitations of multiple databases
**Cross-database relations**
Django doesn’t currently provide any support

**Behavior of contrib apps**
some restrictions
no zuo no die

##Tablespaces
optimizing performance
* Django does not create the tablespaces for you
**Declaring tablespaces for tables**
db_tablespace option inside the model’s class Meta.

**Declaring tablespaces for indexes**
pass the db_tablespace option to a Field constructor

**Database support**
* PostgreSQL and Oracle support

* SQLite and MySQL don’

##Database access optimization
###Profile first
###Use standard DB optimization techniques
* indexes
* field types
### Understand QuerySets
* Understand QuerySet evaluation
* Understand cached attributes
* Use the with template tag
* Use iterator()
### Do database work in the database rather than in Python
### Retrieve individual objects using a unique, indexed column
### Retrieve everything at once if you know you will need it
* Use QuerySet.select_related() and prefetch_related()
### Don’t retrieve things you don’t need
**Use QuerySet.values() and values_list()**
just want a dict or list of values, and don’t need ORM model objects
**Use QuerySet.defer() and only()**
you know that you won’t need
**Use QuerySet.count()**
only want the count
**Use QuerySet.exists()**
only want to find out if at least one result exists
**Don’t overuse count() and exists()**
sometimes
**Use QuerySet.update() and delete()**
**Use foreign key values directly**
**Don’t order results if you don’t care**
### Insert in bulk
reduce the number of SQL queries

##Examples of model relationship API usage##
* Many-to-many relationships
ManyToManyField
* Many-to-one relationships
ForeignKey
* One-to-one relationships
OneToOneField

# Handling HTTP requests

## URL dispatcher
### How Django processes a request
### Example
### Named groups
* If there are any named arguments, it will use those
### What the URLconf searches against
This does not include GET or POST parameters, or the domain name
### Captured arguments are always strings
### Specifying defaults for view arguments
### Performance
urlpatterns is compiled the first time it’s accessed
### Syntax of the urlpatterns variable
a Python list of url() instances
### Error handling
Such values can be set in your root URLconf. Setting these variables in any other URLconf will have no effect
### Including other URLconfs
urlpatterns can “include” other URLconf modules
* Captured parameters
An included URLconf receives any captured parameters from parent URLconfs
### Nested arguments
**only capture the values the view needs to work with and use non-capturing arguments when the regular expression needs an argument but the view ignores it**
### Passing extra options to view functions
an optional third argument which should be a dictionary
* Passing extra options to include()
### Reverse resolution of URLs
performing URL reversing
1. In templates: Using the url template tag.
2. In Python code: Using the reverse() function.
3. In higher level code related to handling of URLs of Django model instances: The get_absolute_url() method.
* Examples
### Naming URL patterns
Putting a prefix on your URL names
### URL namespaces
* Introduction
1. application namespace
2. instance namespace
**Namespaced URLs are specified using the ':' operator**
### Reversing namespaced URLs
1. matching application namespace
2. If there is, URL resolver for that instance
3. If there is no, default application instance is the instance that has an instance namespace matching the application namespace
4. If there is no default application instance, pick the last deployed, whatever its instance name
5. If the provided namespace doesn’t match an application namespace in step 1, Django will attempt a direct lookup of the namespace as an instance namespace
### URL namespaces and included URLconfs
* pass the actual module, or a string reference to the module, to include(), not the list of urlpatterns itself
* include() a 2-tuple containing (<list of url() instances>, <application namespace>)

## Writing views
### A simple view
### Mapping URLs to views
### Returning errors
### The Http404 exception
### Customizing error views

## View decorators
### Allowed HTTP methods
### Conditional view processing
### GZip compression
### Vary headers
### Caching

## File Uploads
### Basic file uploads
a simple form containing a FileField
### Handling uploaded files with a model
using a ModelForm
### Uploading multiple files
override the post method of your FormView subclass to
### Upload Handlers
* Where uploaded data is stored
1. is smaller than 2.5 megabytes, in memory
2. temporary directory
### Changing upload handler behavior
### Modifying upload handlers on the fly
1. insert, request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
2. assign, request.upload_handlers = [ProgressBarUploadHandler(request)]

## Django shortcut functions
render(request, template_name, context=None, content_type=None, status=None, using=None)[source]
### Optional arguments
### render_to_response()
not recommended
### redirect()
### get_object_or_404()
Calls get() on a given model manager, but it raises Http404 instead of the model’s DoesNotExist exception
### get_list_or_404()
Returns the result of filter() on a given model manager cast to a list, raising Http404 if the resulting list is empty.

## Generic views

## Middleware
Middleware is a framework of hooks into Django’s request/response processing. 
It’s a light, low-level “plugin” system for `globally` altering Django’s input or output

### Writing your own middleware
A middleware factory is a callable that takes a get_response callable and returns a middleware

### Marking middleware as unused
middleware’s __init__() method may raise MiddlewareNotUsed

### Activating middleware
add it to the MIDDLEWARE list in your Django settings
**The order in MIDDLEWARE matters because a middleware can depend on other middleware.** 

### Middleware order and layering
think of it like an onion: each middleware class is a “layer” that wraps the view

### Other middleware hooks
three other special methods to class-based middleware
1. process_view()
2. process_exception()
3. process_template_response()

### Dealing with streaming responses
they must test for streaming responses

### Exception handling
automatically converts exceptions

## How to use sessions
contain a session ID – not the data itself (unless you’re using the cookie based backend).

### Enabling sessions
Edit the MIDDLEWARE setting

### Configuring the session engine
* Using database-backed sessions
* Using cached sessions
have multiple caches
**how to store data**
1. may not be persistent
2. For persistent

### Using file-based sessions

### Using cookie-based sessions

### Using sessions in views
read it and write to request.session at any point in your view
* Session serialization
default , json
**Write your own serializer**
store more advanced data types including datetime and Decimal

### Session object guidelines

### Setting test cookies
Django provides an easy way to test whether the user’s browser accepts cookies

### Using sessions out of views

### When sessions are saved
By default, Django only saves to the session database when the session has been modified – 
that is if any of its dictionary values have been assigned or deleted
we can **tell the session object explicitly** that it has been modified 
by setting the modified attribute on the session object

### Browser-length sessions vs. persistent sessions
* don’t want people to have to log in every time they open a browser
* have to log in every time they open a browser

### Clearing the session store

### Settings

### Session security

### Technical details
* The SessionStore object

### Extending database-backed session engines
by inheriting AbstractBaseSession and either SessionStore class

### Session IDs in URLs
It does not fall back to putting session IDs in URLs as a last resort, as PHP does

# Form

## Working with forms
In HTML, a form is a collection of elements inside <form>...</form> 
GET and POST are the only HTTP methods to use when dealing with forms
### Django’s role in forms
### Forms in Django
* The Django Form class
* Instantiating, processing, and rendering forms
### Building a form
### Building a form in Django
### More about Django Form classes
Bound and unbound form instances
1. An unbound form has no data
2. can be used to tell if that data is valid
### Working with form templates

## Formsets
It can be best compared to a data grid
The number of empty forms that is displayed is controlled by the extra parameter
### Using initial data with a formset
ArticleFormSet(request.POST, initial=[...]).
### Limiting the maximum number of forms
ArticleFormSet = formset_factory(ArticleForm, extra=2, max_num=1)
* max_num
* extra
* initial
### Formset validation
BaseFormSet.total_error_count()
* Understanding the ManagementForm
the additional data (form-TOTAL_FORMS, form-INITIAL_FORMS and form-MAX_NUM_FORMS)
* total_form_count : the total number of forms
* initial_form_count : pre-filled
* empty_form : returns a form instance with a prefix of __prefix__ for easier use in dynamic forms with JavaScript
### Custom formset validation
clean method
### Validating the number of forms in a formset
Django provides a couple ways to validate the minimum or maximum number of submitted forms
* validate_max
* validate_min
### Dealing with ordering and deletion of forms
* can_order  Default: False
* can_delete Default: False
1. If you are using a ModelFormSet, model instances for deleted forms will be deleted when you call formset.save().
2. If you call formset.save(`commit=False`), objects `will not be deleted` automatically. You’ll need to call delete() on each of the formset.deleted_objects to actually delete them
### Adding additional fields to a formset
add_fields, simply override this method
### Passing custom parameters to formset forms
* pass this parameter when instantiating the formset
* The formset base class provides a get_form_kwargs method. The method takes a single argument - the index of the form in the formset
### Using a formset in views and templates
Manually rendered can_delete and can_order
### Using more than one formset in a view
you need to pass prefix on both the POST and non-POST cases

## Creating forms from models
ModelForm **Field types**
### Validation on a ModelForm
* Overriding the clean() method
* Interaction with model validation
* Considerations regarding model’s error_messages
override the error messages from NON_FIELD_ERRORS raised by model validation by adding the NON_FIELD_ERRORS key to the error_messages dictionary of the ModelForm’s inner Meta class
### The save() method
Calling save_m2m() is only required if you use save(commit=False)
### Selecting the fields to use
strongly recommended that you explicitly set all fields
### Overriding the default fields
* specify a custom widget for a field, use the widgets attribute of the inner Meta class
* specify the labels, help_texts and error_messages attributes of the inner Meta class 
* specify field_classes to customize the type of fields instantiated by the form
* specify a field’s validators, you can do so by defining the field declaratively and setting its validators parameter
### Enabling localization of fields
By default, the fields in a ModelForm will not localize their data. To enable localization for fields, you can use the localized_fields attribute on the Meta class
### Form inheritance
* declare extra fields or extra methods on a parent class
* subclass the parent’s Meta inner class if you want to change the Meta.fields or Meta.exclude lists
a couple of things to note
* If you have multiple base classes that declare a Meta inner class, only the first one will be used
* ensure that ModelForm appears first in the MRO
* declaratively remove a Field
### Providing initial values
specifying an initial parameter when instantiating the form
### ModelForm factory function
using the standalone function modelform_factory(), instead of using a class definition
* make simple modifications to existing forms
* specified using the fields and exclude keyword arguments
### Model formsets
Like regular formsets, Django provides a couple of enhanced formset classes that make it easy to work with Django models
* Changing the queryset
### Changing the form
### Specifying widgets to use in the form with widgets
### Enabling localization for fields with localized_fields
### Providing initial values
However, with model formsets, the initial values only apply to extra forms, those that aren’t attached to an existing model instance
### Saving objects in the formset
### Limiting the number of editable objects
use the max_num and extra parameters to modelformset_factory() to limit the number of extra forms displayed
A max_num value of None (the default) puts a high limit on the number of forms displayed (1000)
### Using a model formset in a view
very similar to formsets
### Overriding clean() on a ModelFormSet
If you wish to modify a value in ModelFormSet.clean() you must modify form.instance:
### Using a custom queryset
### Using the formset in the template
### Inline formsets
Inline formsets is a small abstraction layer on top of model formsets
### Overriding methods on an InlineFormSet
you should subclass BaseInlineFormSet
### More than one foreign key to the same model
use fk_name to inlineformset_factory()
### Using an inline formset in a view
provide a view that allows a user to edit the related objects of a model
### Specifying widgets to use in the inline form
you can use the widgets parameter in much the same way as passing it to modelformset_factory

## Form Assets (the Media class)
### Assets as a static definition
The easiest way to define assets is as a static definition
Using this method, the declaration is an inner Media class. The properties of the inner class define the requirements
### extend
A boolean defining inheritance behavior for Media declarations.
### Media as a dynamic property
perform some more sophisticated manipulation of asset requirements
### Paths in asset definitions
To find the appropriate prefix to use, Django will check if the STATIC_URL setting is not None and automatically fall back to using MEDIA_URL
### Media objects
use the subscript operator to filter out a medium of interest
print(w.media['css'])
### Combining Media objects
print(w1.media + w2.media)
### Media on Forms
all Form objects have a media property

## Templates
### Support for template engines
* Configuration
The settings.py generated by the startproject command defines a more useful value
### Usage
you can use configured engines directly
### Built-in backends
Set BACKEND to 'django.template.backends.jinja2.Jinja2' to configure a Jinja2 engine
### Custom backends
implement a custom template backend in order to use another template system
### Debug integration for custom engines
* The postmortem appears when TemplateDoesNotExist is raised
* Contextual line information
### Origin API and 3rd-party integration
Custom engines can provide their own template.origin information
### The Django template language
* Syntax
* Variables
{{ first_name }}
* Tags
{% csrf_token %}
* Filters
{{ django|title }}
* Comments
{# this won't be rendered #}
### Components
* Engine
encapsulates an instance of the Django template system
* Template
represents a compiled template
* Context
holds some metadata in addition to the context data
* Loaders
Template loaders are responsible for locating templates, loading them, and returning Template objects
* Context processors
Context processors are functions that receive the current HttpRequest as an argument and return a dict of data to be added to the rendering context

# Class-based views
* structure your views and reuse code by harnessing inheritance and mixins
* TemplateView is a class, not a function, so we point the URL to the as_view() class method instead
* CPU time and bandwidth 

## Introduction to class-based views
### Using class-based views
* url(r'^about/$', GreetingView.as_view(greeting="G'day")),
* def get(self, request):
### Using mixins
Mixins are a form of multiple inheritance where behaviors and attributes of multiple parent classes can be combined
### Handling forms with class-based views
def get(self, request, *args, **kwargs):
def post(self, request, *args, **kwargs):
### Decorating class-based views
* Decorating in URLconf
The simplest way of decorating class-based views is to decorate the result of the as_view() method. 
The easiest place to do this is in the URLconf where you deploy your view
* Decorating the class
apply the decorator to the dispatch() method of the class
transform it into a method decorator first
you can define a list or tuple of decorators 

## Built-in class-based generic views
1. Display list and detail pages for a single object
2. Present date-based objects in year/month/day archive pages
3. Allow users to create, update, and delete objects – with or without authorization
### Extending generic views
### Generic views of objects
* Making “friendly” template contexts
The context_object_name attribute on a generic view specifies the context variable to use
### Adding extra context
provide your own implementation of the get_context_data method
_context_object_name_
### Viewing subsets of objects
using queryset to define a filtered list of objects 
_template_name_
### Dynamic filtering
The key part to making this work is that when class-based views are called, various useful things are stored on self; 
as well as the request (self.request) this includes **the positional (self.args)** 
and **name-based (self.kwargs) arguments** captured according to the URLconf
### Performing extra work

## Form handling with class-based views
* Initial GET (blank or prepopulated form)
* POST with invalid data (typically redisplay form with errors)
* POST with valid data (process the data and typically redirect)
### Model forms
### Models and request.user

## Using mixins with class-based views
Context and template responses
* TemplateResponseMixin
* ContextMixin
### Building up Django’s generic class-based views
* DetailView: working with a single Django object
* ListView: working with many Django objects
### Using Django’s class-based view mixins
* Using SingleObjectMixin with View
* Using SingleObjectMixin with ListView
### Avoid anything more complex
* Using FormMixin with DetailView
### A better solution
### An alternative better solution

# Migrations
## The Commands
* migrate, which is responsible for applying and unapplying migrations.
* makemigrations, which is responsible for creating new migrations based on the changes you have made to your models.
* sqlmigrate, which displays the SQL statements for a migration.
* showmigrations, which lists a project’s migrations and their status.
### Backend Support
* PostgreSQL
the most capable
* MySQL
lacks support for transactions around schema alteration operations
* SQLite
very little
### Workflow
1. Make changes to your models and then run makemigrations
```
$python manage.py makemigrations
```
2. Once you have your new migration files
```
$python manage.py migrate
```
* Version control
go in and modify the migrations yourself
### Dependencies
This dependency behavior affects most migration operations where you restrict to a single app. Restricting to a single app (either in makemigrations or migrate) is a best-efforts promise, and not a guarantee; any other apps that need to be used to get dependencies correct will be.
### Migration files
These files are actually just normal Python files with an agreed-upon object layout, written in a declarative style
* dependencies
* operations
**Custom fields**
if you need a new argument, please create a keyword argument and add something like assert 'argument_name' in kwargs in the constructor
### Model managers
* optionally serialize managers into migrations and have them available in RunPython operations
* If you are using the from_queryset() function to dynamically generate a manager class, you need to inherit from the generated class to make it importable
### Initial migrations
**migrate --fake-initial**
### History consistency
using multiple databases, you can use the allow_migrate() method of database routers to control which databases makemigrations checks for consistent history
### Adding migrations to apps
If your app already has models and database tables, and doesn’t have migrations yet
, you’ll need to convert it to use migrations; this is a simple process:
### Historical models
### Considerations when removing model fields
Add the system_check_deprecated_details attribute to your model field 
### Data Migrations
1. To start, make an empty migration file
2. Let’s write the file
3. python manage.py migrate
* Accessing models from other apps
### More advanced migrations
### Squashing migrations
Squashing is the act of reducing an existing set of many migrations down to one (or sometimes a few) migrations which still represent the same changes
### Serializing values
* Adding a deconstruct() method
### Supporting Python 2 and 3
### Supporting multiple Django versions
If you are the maintainer of a third-party app with models, you may need to ship migrations that support multiple Django versions

# Managing files
By default, Django stores files locally, using the MEDIA_ROOT and MEDIA_URL settings
### Using files in models
* name
* path
* url
### The File object
### File storage
Django’s default file storage is given by the DEFAULT_FILE_STORAGE setting
**Storage objects**
can use the global default storage system
### The built-in filesystem storage class
store uploaded files under /media/photos regardless of what your MEDIA_ROOT setting is

# Testing in Django

## Writing and running tests
### Writing tests
Django’s unit tests use a Python standard library module: unittest
### Running tests
```
$ ./manage.py test
```
**The test database**
### Order in which tests are executed
1. All TestCase subclasses are run first
2. all other Django-based tests
3. Then any other unittest.TestCase tests
### Rollback emulation
Django can reload that data for you on a per-testcase basis by setting the serialized_rollback option to True in the body of the TestCase or TransactionTestCase
### Other test conditions
all Django tests run with DEBUG=False
### Understanding the test output
### Speeding up the tests
* Running tests in parallel
As long as your tests are properly isolated, you can run them in parallel to gain a speed up on multi-core hardware
* Password hashing
set the PASSWORD_HASHERS setting to a faster hashing algorithm

## Testing tools
### The test client
The test client is a Python class that acts as a dummy Web browser, allowing you to test your views and interact with your Django-powered application programmatically
### Overview and a quick example
instantiate Client from within a session of the Python interactive interpreter
### Making requests
Use the django.test.Client class to make requests
### Testing responses
The get() and post() methods both return a Response object. This Response object is not the same as the HttpResponse object returned by Django views; the test response object has some additional data useful for test code to verify
### Exceptions
some exceptions that are not visible to the test client
### Persistent state
The test client is stateful
A test client has two attributes that store persistent state information. You can access these properties as part of a test condition
### Setting the language
1. self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: 'fr'})
2. response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='fr')
3. with translation.override('fr'):
### Provided test case classes
a few extensions of this base class
### SimpleTestCase
A subclass of unittest.TestCase that adds this functionality
### TransactionTestCase
inherits from SimpleTestCase to add some database-specific 
### TestCase
This is the most common class to use for writing tests in Django. It inherits from TransactionTestCase 
### LiveServerTestCase
allows the use of automated test clients other than the Django dummy client
To demonstrate how to use LiveServerTestCase, let’s write a simple Selenium test
### Test cases features
#### Default test client
**SimpleTestCase.client**
This client is recreated for each test
### Customizing the test client
**SimpleTestCase.client_class**
### Fixture loading
A fixture is a collection of data that Django knows how to import into a database
### URLconf configuration
your tests can’t rely upon the fact
### Multi-database support
multi_db = True, flush all the test databases before running test,,,view
### Overriding settings
### Emptying the test outbox
### Assertions
### Tagging tests
You can tag your tests so you can easily run a particular subset
### Email services
automatically redirects all Django-sent email to a dummy outbox
### Management Commands
Management commands can be tested with the call_command() function. The output can be redirected into a StringIO instance
### Skipping tests
check the capabilities of the database, and skip the test if the database doesn’t support a specific named feature

## Advanced testing topics
### The request factory
you can test a view function the same way as you would test any other function
a slightly restricted
### Tests and multiple databases
#### Testing primary/replica configurations
### Controlling creation order for test databases
you can specify the dependencies that exist using the DEPENDENCIES test setting
### Advanced features of TransactionTestCase
* TransactionTestCase.available_apps
a private API. It may be changed or removed
It’s used to optimize Django’s own test suite
* TransactionTestCase.reset_sequences
make sure sequences are always reset before the test run
### Using the Django test runner to test reusable applications
use the Django test runner to run your own test suite
you can add command-line options for controlling verbosity, passing in specific test labels to run
### Using different testing frameworks
#### Defining a test runner
### Testing utilities
### Integration with coverage.py
check the coverage of your tests.

# User authentication in Django
* user accounts
* groups
* permissions
* cookie-based user sessions
### Overview
1. authentication verifies a user is who they claim to be
2. authorization determines what an authenticated user is allowed to do
#### The auth system consists of:
* Users
* Permissions: Binary (yes/no) flags designating whether a user may perform a certain task.
* Groups: A generic way of applying labels and permissions to more than one user.
* A configurable password hashing system
* Forms and view tools for logging in users, or restricting content
* A pluggable backend system
#### third-party packages
* Password strength checking
* Throttling of login attempts
* Authentication against third-parties (OAuth, for example)
### Installation

## Using the Django authentication system
### User objects
**Creating users**
### Creating superusers
### Changing passwords
set_password():
### Authenticating users
### Permissions and Authorization
Permissions can be set not only per type of object, but also per specific object instance
### Default permissions
### Groups
A user in a group automatically has the permissions granted to that group
### Programmatically creating permissions
While custom permissions can be defined within a model’s Meta class, you can also create permissions directly
### Permission caching
If you are adding permissions and checking them immediately afterward, in a test or view for example, the easiest solution is to re-fetch the user from the database
### Authentication in Web requests
#### How to log a user in
**Selecting the authentication backend**
#### How to log a user out
### Limiting access to logged-in users
1. The raw way
The simple, raw way to limit access to pages is to check request.user.is_authenticated and either redirect to a login page
2. The login_required decorator
### The LoginRequired mixin
class MyView(LoginRequiredMixin, View):
### Limiting access to logged-in users that pass a test
* you can use the convenient user_passes_test decorator which performs a redirect when the callable returns False
* When using class-based views, you can use the UserPassesTestMixin to do this
### The permission_required decorator
It’s a relatively common task to check whether a user has a particular permission
### The PermissionRequiredMixin mixin
To apply permission checks to class-based views, you can use the PermissionRequiredMixin
### Redirecting unauthorized requests in class-based views
To ease the handling of access restrictions in class-based views, the AccessMixin can be used to redirect a user to the login page or issue an HTTP 403 Forbidden response
### Authentication Views
### All authentication views
### Helper functions
### Built-in forms
### Authentication data in templates
### Managing users in the admin
* Creating users
the main admin index page
* Changing passwords
the password storage details are displayed

## Password management in Django

## Customizing authentication in Django

# Django’s cache framework



