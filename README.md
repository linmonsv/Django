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

##Database transactions
##Multiple databases
##Tablespaces
##Database access optimization
##Examples of model relationship API usage##

