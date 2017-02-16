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

Order of annotate() and values() clauses

##Search
##Managers
##Performing raw SQL queries
##Database transactions
##Multiple databases
##Tablespaces
##Database access optimization
##Examples of model relationship API usage##

