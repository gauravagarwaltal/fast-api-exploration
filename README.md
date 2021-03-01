# Fast API Exploration

Virtualenv is a tool that lets you create an isolated Python environment for your project. It creates an environment that has its own installation directories.

<h2>Installation</h2>
<p>To install virtualenv run:</p>
<code>pip install virtualenv</code>
<br><br>
<p>Go to the Project Directory</p>
<code>cd fast-api-exploration</code>
<br><br>
<p>Set up virtualenv for that project by running:</p>
<code>virtualenv venv</code>
<br><br>
<p>This command creates a <em>venv</em> directory in your project where all dependencies are installed. You need to activate it first though (in every terminal instance where you are working on your project):</p>

<code>source venv/bin/activate</code>
<br><br>
<p>You should see a (venv) appear at the beginning of your terminal prompt indicating that you are working inside the virtualenv.<br><br> Now you can install all packages by running:</p>

<code>pip install -r requirements.txt</code>

<br />
<p>Then run app using:</p>
<code>python main.py</code>
<br><br>