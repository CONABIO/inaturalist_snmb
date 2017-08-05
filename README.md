# Summary

This is the version of inaturalist modified for the multiple purposes of the SNMB project.

# Dependencies

You basically need to install [Ruby](http://www.ruby-lang.org/) (currently on ruby-2.2.0), [Rails](http://rubyonrails.org/), [PostgreSQL](http://www.postgresql.org/), [PostGIS](http://postgis.refractions.net/), and [Elasticsearch](https://www.elastic.co/products/elasticsearch/) to get a minimally operational setup. Most modern *nix package managers will make this pretty simple.

## Mac OS X
* get xcode: http://developer.apple.com/technology/xcode.html
* get homebrew: https://github.com/mxcl/homebrew/wiki/installation

Ruby and rubygems should already be installed in OS X, unless you manually removed them.

```bash
gem install rails
brew install postgis
brew install imagemagick wkhtmltopdf
```

It may be necessary to install the pg gem manually with `env ARCHFLAGS="-arch x86_64" gem install pg` if you run into problems compiling against different architectures later on.  If you hit problems, you can view the arch a particular file was compiled against with `which ruby`.

## Ubuntu

Should be pretty similar except with apt. For troubleshooting, see

* https://github.com/inaturalist/inaturalist/issues/187

If you're running into errors with RGeo, e.g. `RGeo::Error::UnsupportedOperation: Method Geometry#contains? not defined`, make sure you've installed the geos dev libraries, e.g.

```bash
sudo aptitude install libgeos-dev
sudo aptitude install libgeos++-dev
sudo aptitude install libproj-dev
bundle exec gem uninstall rgeo
bundle update rgeo
```

# Set Up the Database

```bash
psql -c "create extension postgis"
psql -c 'create extension "uuid-ossp"'
createdb template_postgis
psql template_postgis -c "UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template_postgis'"
```

Note that this approach depends on leaving the `template` option in the `database.yml` file.  In theory Rails will use `template_postgis` as a template when creating the databases for each environment, and copy all the PostGIS functions over accordingly.  This is particularly important for testing, where the database is constantly getting dropped and re-created.  

If you want to use a separate postgres user to connect you will need to futz with permissions.  Paths to the postgis files vary based on how you set it up.  If you installed it with homebrew, they should be be somewhere like `/usr/local/Cellar/postgis/1.5.2/share/postgis/postgis.sql`. If you installed `postgresql-9.3-postgis-2.1` on Ubuntu, it should be at `/usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql`.

# Installing iNat

```bash
# Get the code
git clone https://github.com/CONABIO/inaturalist_snmb.git
cd inaturalist_snmb/

# Default config should work at first, but you will need to add API keys for things like 3rd party sign in
Use the files in the source code and edit them.

or

cp config/config.yml.example config/config.yml
cp config/database.yml.example config/database.yml
cp config/gmaps_api_key.yml.example config/gmaps_api_key.yml
cp config/smtp.yml.example config/smtp.yml


# Set up your gems
bundle

# Load the schema
rake db:setup

# Load seed data
rails r tools/load_sources.rb 
rails r tools/load_iconic_taxa.rb
rails r "Site.create( name: 'SNMB Testing Site' )"
```
### Elasticsearch
Elasticsearch can be installed using package managers, but for development environments we recommend downloading the latest version directly from the Elasticsearch website and extracting it into the same folder as the checked-out code. There are rake tasks for elasticsearch that assume there exists a folder inaturalist/elasticsearch (so if you really want to install elasticsearch somewhere, minimally symlink the directory to inaturalist/elasticsearch). The downloaded version doesn't need to be 'installed' per se, just downloaded and uncompressed. Visit https://www.elastic.co/downloads/elasticsearch to see the latest version:

```
cd inaturalist
curl -O https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-x.x.x.tar.gz
tar -zxf elasticsearch-x.x.x.tar.gz
mv elasticsearch-x.x.x elasticsearch
rm elasticsearch-x.x.x.tar.gz

# Install the kuromoji analyzer for Chinese / Kanji character support. 
# Version may need to be changed
cd elasticsearch
bin/elasticsearch-plugin install analysis-kuromoji
cd ..

rake es:start
rake es:rebuild
```

With homebrew:

```
brew install elasticsearch
/usr/local/bin/plugin install analysis-kuromoji
```

Upgrading homebrew:

```
brew upgrade elasticsearch
/usr/local/bin/plugin uninstall analysis-kuromoji
/usr/local/bin/plugin install analysis-kuromoji
```

### Start the application
```
# Try it out
rails s

# Don't forget to start Delayed Job, it's very important.
./script/delayed_job
```

# Optional

## Create Test Users, Places, and Observations

```
rails r "User.create( login: 'testerson', password: 'test', password_confirmation: 'test' )"
rails r tools/import_natural_earth_countries.rb
rails r tools/import_us_states.rb
rails r tools/import_us_counties.rb
rails r tools/load_dummy_observations.rb
```

## Some tools for making more test data

```
# import all California plant taxa from Calflora and make county checklists
rails r tools/sync_calflora_lists.rb

# import taxa from CSV, e.g. a lifelist you exported from iNat
rails r tools/taxa_from_csv.rb PATH_TO_CSV

# import taxa, conservation statuses, and listed taxa from NatureServe (need an API key from http://services.natureserve.org/idd/developer/index.jsp)
rails r tools/natureserve_statuses.rb -ct TAXON_NAME -k NATURESERVE_API_KEY

# Add taxon photos for some observed taxa
rails r "Taxon.where('observations_count > 0').limit(100).each(&:set_photo_from_external)"

```

# Production

While this guide won't go into detail on serving the app in production, we will note that there are a few additional dependencies, mostly related to minifying JS and CSS for the asset pipeline:

* Java
* some JS runtime (e.g. nodejs, see https://github.com/sstephenson/execjs)