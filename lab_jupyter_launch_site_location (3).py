{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "3n3ltmfnrqpi",
    "outputId": "a2d4f52a-2fb7-4668-f5f0-fe862aab8eb0",
    "papermill": {
     "duration": 1.489571,
     "end_time": "2020-09-19T06:26:57.168979",
     "exception": false,
     "start_time": "2020-09-19T06:26:55.679408",
     "status": "completed"
    },
    "tags": []
   },
   "source": [
    "<p style=\"text-align:center\">\n",
    "    <a href=\"https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2022-01-01\" target=\"_blank\">\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png\" width=\"200\" alt=\"Skills Network Logo\"  />\n",
    "    </a>\n",
    "</p>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# **Launch Sites Locations Analysis with Folium**\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Estimated time needed: **40** minutes\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The launch success rate may depend on many factors such as payload mass, orbit type, and so on. It may also depend on the location and proximities of a launch site, i.e., the initial position of rocket trajectories. Finding an optimal location for building a launch site certainly involves many factors and hopefully we could discover some of the factors by analyzing the existing launch site locations.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "In the previous exploratory data analysis labs, you have visualized the SpaceX launch dataset using `matplotlib` and `seaborn` and discovered some preliminary correlations between the launch site and success rates. In this lab, you will be performing more interactive visual analytics using `Folium`.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Objectives\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This lab contains the following tasks:\n",
    "\n",
    "*   **TASK 1:** Mark all launch sites on a map\n",
    "*   **TASK 2:** Mark the success/failed launches for each site on the map\n",
    "*   **TASK 3:** Calculate the distances between a launch site to its proximities\n",
    "\n",
    "After completed the above tasks, you should be able to find some geographical patterns about launch sites.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's first import required Python packages for this lab:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: folium in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (0.11.0)\n",
      "Requirement already satisfied: numpy in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from folium) (1.21.6)\n",
      "Requirement already satisfied: jinja2>=2.9 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from folium) (3.1.2)\n",
      "Requirement already satisfied: requests in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from folium) (2.28.1)\n",
      "Requirement already satisfied: branca>=0.3.0 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from folium) (0.6.0)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from jinja2>=2.9->folium) (2.1.1)\n",
      "Requirement already satisfied: charset-normalizer<3,>=2 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from requests->folium) (2.1.1)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from requests->folium) (2022.9.24)\n",
      "Requirement already satisfied: urllib3<1.27,>=1.21.1 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from requests->folium) (1.26.13)\n",
      "Requirement already satisfied: idna<4,>=2.5 in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (from requests->folium) (3.4)\n",
      "Requirement already satisfied: wget in /home/jupyterlab/conda/envs/python/lib/python3.7/site-packages (3.2)\n"
     ]
    }
   ],
   "source": [
    "!pip3 install folium\n",
    "!pip3 install wget"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import folium\n",
    "import wget\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import folium MarkerCluster plugin\n",
    "from folium.plugins import MarkerCluster\n",
    "# Import folium MousePosition plugin\n",
    "from folium.plugins import MousePosition\n",
    "# Import folium DivIcon plugin\n",
    "from folium.features import DivIcon"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "If you need to refresh your memory about folium, you may download and refer to this previous folium lab:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "[Generating Maps with Python](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module\\_3/DV0101EN-3-5-1-Generating-Maps-in-Python-py-v2.0.ipynb)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Task 1: Mark all launch sites on a map\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "First, let's try to add each site's location on a map using site's latitude and longitude coordinates\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The following dataset with the name `spacex_launch_geo.csv` is an augmented dataset with latitude and longitude added for each site.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Download and read the `spacex_launch_geo.csv`\n",
    "spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')\n",
    "spacex_df=pd.read_csv(spacex_csv_file)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now, you can take a look at what are the coordinates for each site.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Launch Site</th>\n",
       "      <th>Lat</th>\n",
       "      <th>Long</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>CCAFS LC-40</td>\n",
       "      <td>28.562302</td>\n",
       "      <td>-80.577356</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>CCAFS SLC-40</td>\n",
       "      <td>28.563197</td>\n",
       "      <td>-80.576820</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>KSC LC-39A</td>\n",
       "      <td>28.573255</td>\n",
       "      <td>-80.646895</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>VAFB SLC-4E</td>\n",
       "      <td>34.632834</td>\n",
       "      <td>-120.610745</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    Launch Site        Lat        Long\n",
       "0   CCAFS LC-40  28.562302  -80.577356\n",
       "1  CCAFS SLC-40  28.563197  -80.576820\n",
       "2    KSC LC-39A  28.573255  -80.646895\n",
       "3   VAFB SLC-4E  34.632834 -120.610745"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`\n",
    "spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]\n",
    "launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()\n",
    "launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]\n",
    "launch_sites_df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Above coordinates are just plain numbers that can not give you any intuitive insights about where are those launch sites. If you are very good at geography, you can interpret those numbers directly in your mind. If not, that's fine too. Let's visualize those locations by pinning them on a map.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We first need to create a folium `Map` object, with an initial center location to be NASA Johnson Space Center at Houston, Texas.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Start location is NASA Johnson Space Center\n",
    "nasa_coordinate = [29.559684888503615, -95.0830971930759]\n",
    "site_map = folium.Map(location=nasa_coordinate, zoom_start=10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We could use `folium.Circle` to add a highlighted circle area with a text label on a specific coordinate. For example,\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div style=\"width:100%;\"><div style=\"position:relative;width:100%;height:0;padding-bottom:60%;\"><span style=\"color:#565656\">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe srcdoc=\"&lt;!DOCTYPE html&gt;\n",
       "&lt;html&gt;\n",
       "&lt;head&gt;\n",
       "    \n",
       "    &lt;meta http-equiv=&quot;content-type&quot; content=&quot;text/html; charset=UTF-8&quot; /&gt;\n",
       "    \n",
       "        &lt;script&gt;\n",
       "            L_NO_TOUCH = false;\n",
       "            L_DISABLE_3D = false;\n",
       "        &lt;/script&gt;\n",
       "    \n",
       "    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js&quot;&gt;&lt;/script&gt;\n",
       "    &lt;script src=&quot;https://code.jquery.com/jquery-1.12.4.min.js&quot;&gt;&lt;/script&gt;\n",
       "    &lt;script src=&quot;https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js&quot;&gt;&lt;/script&gt;\n",
       "    &lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js&quot;&gt;&lt;/script&gt;\n",
       "    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css&quot;/&gt;\n",
       "    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css&quot;/&gt;\n",
       "    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css&quot;/&gt;\n",
       "    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css&quot;/&gt;\n",
       "    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css&quot;/&gt;\n",
       "    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://rawcdn.githack.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css&quot;/&gt;\n",
       "    &lt;style&gt;html, body {width: 100%;height: 100%;margin: 0;padding: 0;}&lt;/style&gt;\n",
       "    &lt;style&gt;#map {position:absolute;top:0;bottom:0;right:0;left:0;}&lt;/style&gt;\n",
       "    \n",
       "            &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,\n",
       "                initial-scale=1.0, maximum-scale=1.0, user-scalable=no&quot; /&gt;\n",
       "            &lt;style&gt;\n",
       "                #map_7c709c983ffa5553684b2fc4df18b530 {\n",
       "                    position: relative;\n",
       "                    width: 100.0%;\n",
       "                    height: 100.0%;\n",
       "                    left: 0.0%;\n",
       "                    top: 0.0%;\n",
       "                }\n",
       "            &lt;/style&gt;\n",
       "        \n",
       "&lt;/head&gt;\n",
       "&lt;body&gt;\n",
       "    \n",
       "    \n",
       "            &lt;div class=&quot;folium-map&quot; id=&quot;map_7c709c983ffa5553684b2fc4df18b530&quot; &gt;&lt;/div&gt;\n",
       "        \n",
       "&lt;/body&gt;\n",
       "&lt;script&gt;\n",
       "    \n",
       "    \n",
       "            var map_7c709c983ffa5553684b2fc4df18b530 = L.map(\n",
       "                &quot;map_7c709c983ffa5553684b2fc4df18b530&quot;,\n",
       "                {\n",
       "                    center: [29.559684888503615, -95.0830971930759],\n",
       "                    crs: L.CRS.EPSG3857,\n",
       "                    zoom: 10,\n",
       "                    zoomControl: true,\n",
       "                    preferCanvas: false,\n",
       "                }\n",
       "            );\n",
       "\n",
       "            \n",
       "\n",
       "        \n",
       "    \n",
       "            var tile_layer_31f34a5ada8accd0768505b5a0c71814 = L.tileLayer(\n",
       "                &quot;https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png&quot;,\n",
       "                {&quot;attribution&quot;: &quot;Data by \\u0026copy; \\u003ca href=\\&quot;http://openstreetmap.org\\&quot;\\u003eOpenStreetMap\\u003c/a\\u003e, under \\u003ca href=\\&quot;http://www.openstreetmap.org/copyright\\&quot;\\u003eODbL\\u003c/a\\u003e.&quot;, &quot;detectRetina&quot;: false, &quot;maxNativeZoom&quot;: 18, &quot;maxZoom&quot;: 18, &quot;minZoom&quot;: 0, &quot;noWrap&quot;: false, &quot;opacity&quot;: 1, &quot;subdomains&quot;: &quot;abc&quot;, &quot;tms&quot;: false}\n",
       "            ).addTo(map_7c709c983ffa5553684b2fc4df18b530);\n",
       "        \n",
       "    \n",
       "            var circle_7ea0618dc4d861d577ed2b3d99746111 = L.circle(\n",
       "                [29.559684888503615, -95.0830971930759],\n",
       "                {&quot;bubblingMouseEvents&quot;: true, &quot;color&quot;: &quot;#d35400&quot;, &quot;dashArray&quot;: null, &quot;dashOffset&quot;: null, &quot;fill&quot;: true, &quot;fillColor&quot;: &quot;#d35400&quot;, &quot;fillOpacity&quot;: 0.2, &quot;fillRule&quot;: &quot;evenodd&quot;, &quot;lineCap&quot;: &quot;round&quot;, &quot;lineJoin&quot;: &quot;round&quot;, &quot;opacity&quot;: 1.0, &quot;radius&quot;: 1000, &quot;stroke&quot;: true, &quot;weight&quot;: 3}\n",
       "            ).addTo(map_7c709c983ffa5553684b2fc4df18b530);\n",
       "        \n",
       "    \n",
       "        var popup_3baab2096b9030980f6f730423dc5641 = L.popup({&quot;maxWidth&quot;: &quot;100%&quot;});\n",
       "\n",
       "        \n",
       "            var html_42eb4db1a57ca17e8e165bb5876753fe = $(`&lt;div id=&quot;html_42eb4db1a57ca17e8e165bb5876753fe&quot; style=&quot;width: 100.0%; height: 100.0%;&quot;&gt;NASA Johnson Space Center&lt;/div&gt;`)[0];\n",
       "            popup_3baab2096b9030980f6f730423dc5641.setContent(html_42eb4db1a57ca17e8e165bb5876753fe);\n",
       "        \n",
       "\n",
       "        circle_7ea0618dc4d861d577ed2b3d99746111.bindPopup(popup_3baab2096b9030980f6f730423dc5641)\n",
       "        ;\n",
       "\n",
       "        \n",
       "    \n",
       "    \n",
       "            var marker_bd037595cc5434c1becf94000729abc6 = L.marker(\n",
       "                [29.559684888503615, -95.0830971930759],\n",
       "                {}\n",
       "            ).addTo(map_7c709c983ffa5553684b2fc4df18b530);\n",
       "        \n",
       "    \n",
       "            var div_icon_43e5bf62d42bc7d068b7aa68a4465f8e = L.divIcon({&quot;className&quot;: &quot;empty&quot;, &quot;html&quot;: &quot;\\u003cdiv style=\\&quot;font-size: 12; color:#d35400;\\&quot;\\u003e\\u003cb\\u003eNASA JSC\\u003c/b\\u003e\\u003c/div\\u003e&quot;, &quot;iconAnchor&quot;: [0, 0], &quot;iconSize&quot;: [20, 20]});\n",
       "            marker_bd037595cc5434c1becf94000729abc6.setIcon(div_icon_43e5bf62d42bc7d068b7aa68a4465f8e);\n",
       "        \n",
       "&lt;/script&gt;\n",
       "&lt;/html&gt;\" style=\"position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;\" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>"
      ],
      "text/plain": [
       "<folium.folium.Map at 0x7fb21c0cc150>"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name\n",
    "circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))\n",
    "# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name\n",
    "marker = folium.map.Marker(\n",
    "    nasa_coordinate,\n",
    "    # Create an icon as a text label\n",
    "    icon=DivIcon(\n",
    "        icon_size=(20,20),\n",
    "        icon_anchor=(0,0),\n",
    "        html='<div style=\"font-size: 12; color:#d35400;\"><b>%s</b></div>' % 'NASA JSC',\n",
    "        )\n",
    "    )\n",
    "site_map.add_child(circle)\n",
    "site_map.add_child(marker)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "and you should find a small yellow circle near the city of Houston and you can zoom-in to see a larger circle.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now, let's add a circle for each launch site in data frame `launch_sites`\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*TODO:*  Create and add `folium.Circle` and `folium.Marker` for each launch site on the site map\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "An example of folium.Circle:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "`folium.Circle(coordinate, radius=1000, color='#000000', fill=True).add_child(folium.Popup(...))`\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "An example of folium.Marker:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "`folium.map.Marker(coordinate, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0), html='<div style=\"font-size: 12; color:#d35400;\"><b>%s</b></div>' % 'label', ))`\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "EOL while scanning string literal (2163899829.py, line 15)",
     "output_type": "error",
     "traceback": [
      "\u001b[0;36m  File \u001b[0;32m\"/tmp/ipykernel_2291/2163899829.py\"\u001b[0;36m, line \u001b[0;32m15\u001b[0m\n\u001b[0;31m    html='\u001b[0m\n\u001b[0m          ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m EOL while scanning string literal\n"
     ]
    }
   ],
   "source": [
    "# Initial the map\n",
    "site_map = folium.Map(location=nasa_coordinate, zoom_start=5)\n",
    "# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label\n",
    "for launch_site, site_lat, site_long in zip(launch_sites_df['Launch Site'], launch_sites_df['Lat'], launch_sites_df['Long']):\n",
    "    site_coordinate = [site_lat, site_long]\n",
    "    \n",
    "    circle = folium.Circle(site_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup(launch_site))\n",
    "    \n",
    "    marker = folium.map.Marker(\n",
    "        site_coordinate,\n",
    "        # Create an icon as a text label\n",
    "        icon=DivIcon(\n",
    "            icon_size=(20, 20),\n",
    "            icon_anchor=(0, 0),\n",
    "            html='\n",
    "%s\n",
    "' % launch_site,\n",
    "            )\n",
    "        )\n",
    "    site_map.add_child(circle)\n",
    "    site_map.add_child(marker)\n",
    "site_map"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The generated map with marked launch sites should look similar to the following:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<center>\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_markers.png\" />\n",
    "</center>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now, you can explore the map by zoom-in/out the marked areas\n",
    ", and try to answer the following questions:\n",
    "\n",
    "*   Are all launch sites in proximity to the Equator line?\n",
    "*   Are all launch sites in very close proximity to the coast?\n",
    "\n",
    "Also please try to explain your findings.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Task 2: Mark the success/failed launches for each site on the map\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next, let's try to enhance the map by adding the launch outcomes for each site, and see which sites have high success rates.\n",
    "Recall that data frame spacex_df has detailed launch records, and the `class` column indicates if this launch was successful or not\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "spacex_df.tail(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next, let's create markers for all launch records.\n",
    "If a launch was successful `(class=1)`, then we use a green marker and if a launch was failed, we use a red marker `(class=0)`\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Note that a launch only happens in one of the four launch sites, which means many launch records will have the exact same coordinate. Marker clusters can be a good way to simplify a map containing many markers having the same coordinate.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's first create a `MarkerCluster` object\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "wP9PVUZ7Jfjt",
    "outputId": "6a3b8164-940c-4b93-9f3d-c655c4a0c683",
    "papermill": {
     "duration": 0.904519,
     "end_time": "2020-09-19T06:27:38.357041",
     "exception": false,
     "start_time": "2020-09-19T06:27:37.452522",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "marker_cluster = MarkerCluster().add_to(site_map)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*TODO:* Create a new column in `launch_sites` dataframe called `marker_color` to store the marker colors based on the `class` value\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# Apply a function to check the value of `class` column\n",
    "# If class=1, marker_color value will be green\n",
    "# If class=0, marker_color value will be red\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Function to assign color to launch outcome\n",
    "def assign_marker_color(launch_outcome):\n",
    "    if launch_outcome == 1:\n",
    "        return 'green'\n",
    "    else:\n",
    "        return 'red'\n",
    "    \n",
    "spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)\n",
    "spacex_df.tail(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*TODO:* For each launch result in `spacex_df` data frame, add a `folium.Marker` to `marker_cluster`\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Initial the map\n",
    "site_map = folium.Map(location=nasa_coordinate, zoom_start=5)\n",
    "# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label\n",
    "for launch_site, site_lat, site_long in zip(launch_sites_df['Launch Site'], launch_sites_df['Lat'], launch_sites_df['Long']):\n",
    "    site_coordinate = [site_lat, site_long]\n",
    "    \n",
    "    circle = folium.Circle(site_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup(launch_site))\n",
    "    \n",
    "    marker = folium.map.Marker(\n",
    "        site_coordinate,\n",
    "        # Create an icon as a text label\n",
    "        icon=DivIcon(\n",
    "            icon_size=(20, 20),\n",
    "            icon_anchor=(0, 0),\n",
    "            html='\n",
    "%s\n",
    "' % launch_site,\n",
    "            )\n",
    "        )\n",
    "    site_map.add_child(circle)\n",
    "    site_map.add_child(marker)\n",
    "site_map"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Your updated map may look like the following screenshots:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<center>\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_marker_cluster.png\" />\n",
    "</center>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<center>\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_marker_cluster_zoomed.png\" />\n",
    "</center>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "From the color-labeled markers in marker clusters, you should be able to easily identify which launch sites have relatively high success rates.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# TASK 3: Calculate the distances between a launch site to its proximities\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next, we need to explore and analyze the proximities of launch sites.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's first add a `MousePosition` on the map to get coordinate for a mouse over a point on the map. As such, while you are exploring the map, you can easily find the coordinates of any points of interests (such as railway)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map\n",
    "formatter = \"function(num) {return L.Util.formatNum(num, 5);};\"\n",
    "mouse_position = MousePosition(\n",
    "    position='topright',\n",
    "    separator=' Long: ',\n",
    "    empty_string='NaN',\n",
    "    lng_first=False,\n",
    "    num_digits=20,\n",
    "    prefix='Lat:',\n",
    "    lat_formatter=formatter,\n",
    "    lng_formatter=formatter,\n",
    ")\n",
    "\n",
    "site_map.add_child(mouse_position)\n",
    "site_map"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc. Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "You can calculate the distance between two points on the map based on their `Lat` and `Long` values using the following method:\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from math import sin, cos, sqrt, atan2, radians\n",
    "\n",
    "def calculate_distance(lat1, lon1, lat2, lon2):\n",
    "    # approximate radius of earth in km\n",
    "    R = 6373.0\n",
    "\n",
    "    lat1 = radians(lat1)\n",
    "    lon1 = radians(lon1)\n",
    "    lat2 = radians(lat2)\n",
    "    lon2 = radians(lon2)\n",
    "\n",
    "    dlon = lon2 - lon1\n",
    "    dlat = lat2 - lat1\n",
    "\n",
    "    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2\n",
    "    c = 2 * atan2(sqrt(a), sqrt(1 - a))\n",
    "\n",
    "    distance = R * c\n",
    "    return distance"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*TODO:* Mark down a point on the closest coastline using MousePosition and calculate the distance between the coastline point and the launch site.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# find coordinate of the closet coastline\n",
    "# distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)\n",
    "\n",
    "launch_site_lat, launch_site_lon = 28.563197, -80.576820\n",
    "coastline_lat, coastline_lon = 28.56319, -80.56785\n",
    "\n",
    "distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)\n",
    "distance_coastline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*TODO:* After obtained its coordinate, create a `folium.Marker` to show the distance\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create and add a folium.Marker on your selected closest coastline point on the map\n",
    "# Display the distance between coastline point and launch site using the icon property \n",
    "distance_marker = folium.Marker(\n",
    "   location=[coastline_lat, coastline_lon],\n",
    "   icon=DivIcon(\n",
    "       icon_size=(20,20),\n",
    "       icon_anchor=(0,0),\n",
    "       html='<div style=\"font-size: 12; color:#d35400;\"><b>%s</b></div>' % \"{:10.2f} KM\".format(distance_coastline),\n",
    "       )\n",
    "   )"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*TODO:* Draw a `PolyLine` between a launch site to the selected coastline point\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate\n",
    "lines=folium.PolyLine(locations=[[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]], weight=1)\n",
    "site_map.add_child(lines)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Your updated map with distance line should look like the following screenshot:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<center>\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/launch_site_marker_distance.png\" />\n",
    "</center>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "*TODO:* Similarly, you can draw a line betwee a launch site to its closest city, railway, highway, etc. You need to use `MousePosition` to find the their coordinates on the map first\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "A railway map symbol may look like this:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<center>\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/railway.png\" />\n",
    "</center>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "A highway map symbol may look like this:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<center>\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/highway.png\" />\n",
    "</center>\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "A city map symbol may look like this:\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "<center>\n",
    "    <img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/images/city.png\" />\n",
    "</center>\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "city_lat, city_lon = 28.53, -81.38  # coords for Orlando\n",
    "\n",
    "line2=folium.PolyLine(locations=[[launch_site_lat, launch_site_lon], [city_lat, city_lon]], weight=3)\n",
    "site_map.add_child(line2)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "After you plot distance lines to the proximities, you can answer the following questions easily:\n",
    "\n",
    "*   Are launch sites in close proximity to railways?\n",
    "*   Are launch sites in close proximity to highways?\n",
    "*   Are launch sites in close proximity to coastline?\n",
    "*   Do launch sites keep certain distance away from cities?\n",
    "\n",
    "Also please try to explain your findings.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Next Steps:\n",
    "\n",
    "Now you have discovered many interesting insights related to the launch sites' location using folium, in a very interactive way. Next, you will need to build a dashboard using Ploty Dash on detailed launch records.\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Authors\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "[Yan Luo](https://www.linkedin.com/in/yan-luo-96288783/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2022-01-01)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Other Contributors\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Joseph Santarcangelo\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Change Log\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "| Date (YYYY-MM-DD) | Version | Changed By | Change Description          |\n",
    "| ----------------- | ------- | ---------- | --------------------------- |\n",
    "| 2021-05-26        | 1.0     | Yan        | Created the initial version |\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Copyright © 2021 IBM Corporation. All rights reserved.\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python",
   "language": "python",
   "name": "conda-env-python-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.12"
  },
  "papermill": {
   "duration": 142.196942,
   "end_time": "2020-09-19T06:29:13.341578",
   "environment_variables": {},
   "exception": null,
   "input_path": "__notebook__.ipynb",
   "output_path": "__notebook__.ipynb",
   "parameters": {},
   "start_time": "2020-09-19T06:26:51.144636",
   "version": "2.1.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
