# Task 29 --- Product Basket Analysis

## Overview

This project performs product basket (market-basket) analysis on the
Online Retail II dataset to identify products that are frequently
purchased together.

## Objective

-   Identify frequently co-purchased product pairs.
-   Calculate pair frequency and support.
-   Generate simple product recommendations.
-   Extract business insights for cross-selling and bundling.

## Tools & Technologies

-   Python
-   Pandas
-   Matplotlib
-   itertools
-   collections
-   VS Code

## Dataset

**Online Retail II**

Original dataset: - Rows: 1,067,371 - Columns: 8

Relevant fields: - `Invoice` --- order/invoice identifier - `StockCode`
--- product identifier - `Description` --- product description -
`Quantity` --- quantity purchased - `InvoiceDate` - `Price` -
`Customer ID` - `Country`

## Data Cleaning

The analysis: 1. Removed records with missing product descriptions. 2.
Removed cancelled invoices. 3. Removed rows with non-positive
quantities. 4. Cleaned product descriptions. 5. Removed duplicate
product entries within the same invoice.

Clean basket data: - Rows: 996,749 unique invoice-product combinations -
Orders: 40,301 - Unique products: 5,426 - Average unique products per
order: 24.73

## Methodology

For each invoice, unique products were collected into a basket. All
2-product combinations were generated using `itertools.combinations()`.
Self-pairs were excluded by generating combinations of two distinct
products.

For a product pair:

**Frequency** = number of orders containing both products.

**Support (%)** = Frequency / Total Orders × 100

A total of **5,865,911 unique product pairs** were generated.

## Top Product Pairs

  -------------------------------------------------------------------------
  Rank            Product Pair               Frequency              Support
  --------------- --------------- -------------------- --------------------
  1               RED HANGING                    1,240                3.08%
                  HEART T-LIGHT                        
                  HOLDER + WHITE                       
                  HANGING HEART                        
                  T-LIGHT HOLDER                       

  2               WOODEN FRAME                   1,114                2.76%
                  ANTIQUE WHITE +                      
                  WOODEN PICTURE                       
                  FRAME WHITE                          
                  FINISH                               

  3               JUMBO BAG RED                  1,096                2.72%
                  RETROSPOT +                          
                  JUMBO STORAGE                        
                  BAG SUKI                             

  4               STRAWBERRY                     1,052                2.61%
                  CERAMIC TRINKET                      
                  BOX +                                
                  SWEETHEART                           
                  CERAMIC TRINKET                      
                  BOX                                  

  5               GREEN REGENCY                  1,024                2.54%
                  TEACUP AND                           
                  SAUCER + ROSES                       
                  REGENCY TEACUP                       
                  AND SAUCER                           

  6               JUMBO BAG RED                  1,008                2.50%
                  RETROSPOT +                          
                  JUMBO SHOPPER                        
                  VINTAGE RED                          
                  PAISLEY                              

  7               HEART OF WICKER                1,005                2.49%
                  LARGE + HEART                        
                  OF WICKER SMALL                      

  8               JUMBO BAG PINK                   966                2.40%
                  POLKADOT +                           
                  JUMBO BAG RED                        
                  RETROSPOT                            

  9               60 TEATIME                       926                2.30%
                  FAIRY CAKE                           
                  CASES + PACK OF                      
                  60 PINK PAISLEY                      
                  CAKE CASES                           

  10              JUMBO BAG RED                    926                2.30%
                  RETROSPOT +                          
                  JUMBO BAG                            
                  STRAWBERRY                           
  -------------------------------------------------------------------------

## Key Insights

1.  The RED HANGING HEART T-LIGHT HOLDER and WHITE HANGING HEART T-LIGHT
    HOLDER formed the highest-frequency pair, occurring together in
    1,240 orders.
2.  JUMBO BAG RED RETROSPOT appears in multiple high-frequency pairs,
    indicating repeated co-occurrence with other bag designs.
3.  Several high-frequency pairs involve matching, complementary, or
    size-related products.
4.  Decorative items, bags, gift products, and coordinated designs are
    prominent among the frequent associations.
5.  These associations can support "Frequently Bought Together"
    recommendations, cross-selling, bundle creation, and promotional
    placement.
6.  Support provides the proportion of analyzed orders containing a
    pair; it does not by itself establish causation.

## Deliverables

-   `cleaned_basket_data.csv`
-   `all_product_pairs.csv`
-   `top_20_product_pairs.csv`
-   `product_recommendations.csv`
-   `visuals/top_10_product_pairs_frequency.png`
-   `visuals/top_10_product_pairs_support.png`
-   `visuals/top_associated_products.png`

## Project Structure

``` text
Task_29_Product_Basket_Analysis/
├── product_basket_analysis.py
├── data/
│   └── online_retail_II.csv
├── reports/
│   ├── cleaned_basket_data.csv
│   ├── all_product_pairs.csv
│   ├── top_20_product_pairs.csv
│   └── product_recommendations.csv
└── visuals/
    ├── top_10_product_pairs_frequency.png
    ├── top_10_product_pairs_support.png
    └── top_associated_products.png
```

## Conclusion

The analysis successfully identifies frequently co-purchased products
using invoice-level basket analysis. The results provide a practical
foundation for product recommendations and cross-selling strategies.

> Note: Co-occurrence indicates association in the analyzed transaction
> data and should not be interpreted as proof that one product causes
> the purchase of another.
