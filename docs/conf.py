# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys, os

# sys.path.append(os.path.abspath("../"))
sys.path.append('/home/pi/Sensor_Scripts/pygame_code/tricorder/')

# sys.path.append('/home/pi/Sensor_Scripts/pygame_code/tricorder/assets/')
# sys.path.append('/home/pi/Sensor_Scripts/pygame_code/tricorder/assets/saved_fonts/')
# sys.path.append('/home/pi/Sensor_Scripts/pygame_code/tricorder/assets/pics/')
# sys.path.append('/home/pi/Sensor_Scripts/pygame_code/tricorder/sensor_pages/')
# sys.path.append('/home/pi/Sensor_Scripts/pygame_code/tricorder/general_pages/')
# sys.path.append('/home/pi/Sensor_Scripts/pygame_code/tricorder/resources/')

# sys.path.append(os.path.abspath("../assets/"))
# sys.path.append(os.path.abspath("../assets/saved_fonts"))
# sys.path.append(os.path.abspath("../sensor_pages/"))
# sys.path.append(os.path.abspath("../general_pages/"))
# sys.path.append(os.path.abspath("../resources/"))

extensions = ['extname']

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Tricorder-RaspberryPi'
copyright = '2023, Shivam Kundan'
author = 'Shivam Kundan'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store','.png']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
