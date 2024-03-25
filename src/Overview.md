# Automated-product-categorization-for-e-commerce-with-AI

## Industries: 
e-commerce, delivery apps, marketplaces, many others

## Technologies and Tools: 
NLP, Computer Vision, Supervised Learning, Deep Learning, HTTP APIs, TensorFlow, Pytorch, Transformers, Spacy/NLTK, Docker.

## Difficulty level: (4/5)

Creating relevant tags and categories on products allow e-commerce companies (such as Amazon, Wayfair, eBay in the US, Mercado Libre, Dafiti in Latam, or ASOS.com and Zalando in Europe), and super apps and marketplaces (such as Instacart in the US, Rappi, Frubana, JOKR in Latam) to automatically categorize products whether those are new products uploaded by a user or seller products that need large-scale automated categorization. Automation on this subject not only saves time and manual effort but creates a taxonomy system that improves the process of a customer finding what they are looking for, improving their conversion metrics, and activating frictionless and engaging shopping experiences. In this project you will apply natural language processing to create a multi-label system able to classify e-commerce products automatically.

## Goal: 
The main objective of this project is to build a system/service that will accept a typical "new product"  to classify the product into a set of predefined categories.

In order to graduate from the ML Developer Career, you have to approve the Main Deliverables. You are also welcome to complete the Optional Deliverables if you want to continue to add experience and build your portfolio, although those are not mandatory. 

## Main Deliverables:

1. Exploratory Dataset Analysis (EDA) Jupyter notebooks and dataset
2. Scripts used for data pre-processing and data preparation
3. Training scripts and trained models. Description of how to reproduce results
4. Implementation and training of the NLP model for product classification
5. API with a basic UI interface for demo (upload of textual description and return of predictions)
6. Everything must be containerized using Docker

## Optional Objectives:

1. Retraining of model with new data added by users.

## Approach and Milestones
There are many ways to approach this project and at first sight, this might seem very overwhelming. A good rule of thumb is this:

1. Get a good overview and idea of what you need to build.
2. Identify the unknowns and, most importantly, the major risks for the project and allocate time appropriately. For instance: setting up     a dockerized API is simple and low risk but dealing with a dirty dataset is a high-risk task. 
3. Some tasks will take a long time and might be a blocker for other tasks. Try anticipating the unknowns and allocate time as necessary.

## Dataset
The dataset for this project is based on the open e-commerce dataset from BestBuy.com (largest online and brick-and-mortar retailer in the US). The dataset can be downloaded here.

The dataset contains two source files: categories.json and products.json which will be relevant to this project. Both files are small enough to be accessed directly from Github using the following raw URL schema:

https://raw.githubusercontent.com/anyoneai/e-commerce-open-data-set/master/products.json

## References
There are quite a few references and existing models on the internet. Feel free to research as much as you need on the subject. Below you will find a couple of good starting points:

- Large Scale Product Categorization using Structured and Unstructured Attributes - Abhinandan Krishnan, Abilash Amarthaluri
  (https://arxiv.org/abs/1903.04254)
- Multi-Label Product Categorization Using Multi-Modal Fusion Models - Pasawee Wirojwatanakul, Artit Wangperawong
  (https://arxiv.org/abs/1907.00420)

