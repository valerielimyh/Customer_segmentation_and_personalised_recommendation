Online personalised recommendations
===================================

The explosive growth of online content and services has provided a myriad of choices for users. For instance, on e-commerce websites or apps, users are provided an overwhelming volume of products than the amount that users can digest. Therefore, personalized online recommendation are necessary to improve user experience. The corollary of a pleasant user experience is augmented profits for businesses. 

Before curating a set of products for different users, it is imperative to understand them better. Some of your users might make small purchases every week, others might make big purchases once a year—and there all sorts of combinations in between. How can you possibly have foresight on what they might potentially purchase and recommend them accordingly. 

Customer Lifetime Value (CLV) takes some of the mystery out of knowing how your current and future customers will behave. By calculating your CLV, you’ll be able to understand how often certain types of customers will make purchases and when those same customers will stop making purchases for good. The Recency-Frequency-Monetary Value (RFM) model is used to quantify CLV. Three buckets of customers were derived using clustering algorithm – high, mid and low-value customers. Collaborative filtering models were then developed for each bucket of customer using Spark’s Alternating Least Square. Collaborative filtering method is appropriate for existing users, because we have prior knowledge on their CLV. However, we do not know how to quantify the CLV for new users. Hence, a content-based model that recommends popular or trending products is created for them. 

[This is an interim update of my project. Feel free to check back next week for the report :) Feel free to reach out with any questions]


Project Organization
------------

    ├── README.md          
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    │
    ├── models            
    │
    ├── notebooks          
    │                      
    ├── references        
    ├── reports           
    │   └── figures     
    │
    ├── test-campaign   <- build flask app and deploy on Heroku
    │                     

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
