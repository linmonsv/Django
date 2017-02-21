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
##Database access optimization
##Examples of model relationship API usage##

