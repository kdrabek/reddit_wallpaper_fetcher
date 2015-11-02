### reddit_wallpaper_fetcher

This is a simple Python script that fetches wallpapers from Reddit (by default from /r/earthporn). It was created because
I was bored and I have always struggled with finding a decent wallpaper.
It fetches top reddit submissions from a week, then iterates over results and tries to donwload .jpg with proper dimensions.


##### Runnig the script
1. Clone the repo

2. Install dependencies `pip install -r requirements.txt`

3. Run the script: 

``` python wallpapers/wallpapers.py ```

Additionaly, you can pass parameters: 
```python wallpapers/wallpapers.py --subreddit=earthporn --width=1920 --height=1080```

If you don't pass any parameters, the script will assume default settings, that is full HD resolutin and /r/earthporn subreddit.


##### Running the tests
```
py.test --cov-report=term-missing --cov=wallpapers/ tests/
```
