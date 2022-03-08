# PC Donation

A Microsoft-IVE project for PC donation

Support command line

-Initialization- Install Library
<pre><code>pip install -r requirements.txt
pip install azure-ai-formrecognizer --pre
</code></pre>

Database initialization
<pre><code>flask db init
flask db migrate
flask db upgrade
</code></pre>

Database reset
<pre><code>python reset_db.py
flask db upgrade
</code></pre>

Insert required data
<pre><code>python insert_init_data.py
</code></pre>

Export Library
<pre><code>pip freeze > requirements.txt
</code></pre>

Enter vitual environment
<pre><code>. venv/bin/activate
</code></pre>

Translation

Extract all the translated texts to the .pot file
<pre><code>pybabel extract -F babel.cfg -k _l -o messages.pot .
</code></pre>

Generating a Language Catalog
<pre><code>pybabel init -i messages.pot -d app/translations -l zh
</code></pre>

Updating - Please copy messages.po in app/translations
<pre><code>pybabel extract -F babel.cfg -k _l -o messages.pot .
pybabel update -i messages.pot -d app/translations
</code></pre>

After Updating, Please Compile translation to activation translation Compile translation
<pre><code>pybabel compile -d app/translations
</code></pre>

Commang-Line version
<pre><code>flask translate init LANG to add a new language
flask translate update to update all language repositories
flask translate compile to compile all language repositories
</code></pre>
Update

Azure change prod branch azure login
<pre><code>az acr login --name pcdonation.azurecr.io
</code></pre>
docker-compose up down push
<pre><code>docker-compose up --build -d
docker-compose down
docker-compose push
</code></pre>


If you cannot migrate, please modify migrations/env.py .
<pre><code>target_metadata = models.db.Model.metadata
</code></pre>


To reset Database
<pre><code>
python reset_db.py && flask db upgrade && python insert_init_data.py
</code></pre>
