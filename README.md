# Code for https://corona.pw 

Code for deploying https://corona.pw. A website for comparing the effectiveness of Corona Antigen Tests bases on official, scientific data.

PyPDF2 + Camelot for extracting data from the messy `.pdf`.  
Flask + DataTables to serve website with a clean front-end.  

Before running, execute to resolve dependencies: 
```
pip install -r requirements.txt
```

`download_and_convert_data.py` downloads the latest `.pdf` file from [Paul Ehrlich Institut](https://www.pei.de) and writes it to disk. Then, it attempts to extract the tables and writes them to a `.csv` file.  

`app.py` reads the `.csv` table as a DataFrame. Following, it serves it using Flask. The website uses DataTables with a Bootstrap v5 theme to display the data and make it searchable and sortable.  

`wsgi.py` can be used as an entrypoint to serve via uwsgi (or e.g. gunicorn etc.). See also `corona.ini` for a template uwsgi config file.  


## Resources

- Front-end borrows heavily from Miguel Grinberg's [repo](https://github.com/miguelgrinberg/flask-tables)
- [Original Data](https://www.pei.de/SharedDocs/Downloads/DE/newsroom/dossiers/evaluierung-sensitivitaet-sars-cov-2-antigentests.pdf)