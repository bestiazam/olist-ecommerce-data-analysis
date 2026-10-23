-- Olist E-Commerce Data Analysis | MySQL 8+
-- Source: Brazilian E-Commerce Public Dataset by Olist (Kaggle)
-- Run after importing the original Olist CSV tables into olist_project.
USE olist_project;

-- 01 | Table counts
SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM olist_orders_dataset
UNION ALL SELECT 'customers', COUNT(*) FROM olist_customers_dataset
UNION ALL SELECT 'order_items', COUNT(*) FROM olist_order_items_dataset
UNION ALL SELECT 'products', COUNT(*) FROM olist_products_dataset
UNION ALL SELECT 'payments', COUNT(*) FROM olist_order_payments_dataset
UNION ALL SELECT 'reviews', COUNT(*) FROM olist_order_reviews_dataset
UNION ALL SELECT 'sellers', COUNT(*) FROM olist_sellers_dataset
UNION ALL SELECT 'category_translation', COUNT(*) FROM product_category_name_translation;

-- 02 | Order status distribution
SELECT order_status, COUNT(*) AS orders
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY orders DESC;

-- 03 | Monthly order volume
SELECT DATE_FORMAT(STR_TO_DATE(order_purchase_timestamp,'%Y-%m-%d %H:%i:%s'),'%Y-%m') AS order_month,
       COUNT(*) AS orders
FROM olist_orders_dataset
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY order_month ORDER BY order_month;

-- 04 | Top product categories by product revenue (excluding shipping)
SELECT COALESCE(t.product_category_name_english,p.product_category_name,'Uncategorized') AS category,
       ROUND(SUM(i.price),2) AS product_revenue_brl
FROM olist_order_items_dataset i
JOIN olist_products_dataset p ON p.product_id=i.product_id
LEFT JOIN product_category_name_translation t ON t.product_category_name=p.product_category_name
GROUP BY category ORDER BY product_revenue_brl DESC LIMIT 10;

-- 05 | Review score distribution
SELECT review_score, COUNT(*) AS reviews
FROM olist_order_reviews_dataset
GROUP BY review_score ORDER BY review_score DESC;

-- 06 | Payment types: payment records and payment amounts
SELECT payment_type, COUNT(*) AS payment_records,
       ROUND(SUM(payment_value),2) AS payment_value_brl
FROM olist_order_payments_dataset
GROUP BY payment_type ORDER BY payment_value_brl DESC;

-- 07 | Delivery punctuality among delivered orders with both dates
SELECT CASE
  WHEN STR_TO_DATE(order_delivered_customer_date,'%Y-%m-%d %H:%i:%s')
       <= STR_TO_DATE(order_estimated_delivery_date,'%Y-%m-%d %H:%i:%s') THEN 'On time'
  ELSE 'Late' END AS delivery_status,
  COUNT(*) AS orders
FROM olist_orders_dataset
WHERE order_status='delivered'
 AND order_delivered_customer_date IS NOT NULL
 AND order_estimated_delivery_date IS NOT NULL
GROUP BY delivery_status;

-- 08 | Revenue and shipping KPIs at order-item level
SELECT COUNT(*) AS order_item_rows,
       ROUND(SUM(price),2) AS product_revenue_brl,
       ROUND(SUM(freight_value),2) AS shipping_charges_brl,
       ROUND(AVG(price),2) AS average_item_price_brl
FROM olist_order_items_dataset;

-- 09 | Customer cities with highest order counts
SELECT c.customer_city, COUNT(*) AS orders
FROM olist_orders_dataset o
JOIN olist_customers_dataset c ON o.customer_id=c.customer_id
GROUP BY c.customer_city ORDER BY orders DESC LIMIT 10;

-- 10 | Repeat customers: use customer_unique_id, not customer_id
SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS orders
FROM olist_orders_dataset o
JOIN olist_customers_dataset c ON o.customer_id=c.customer_id
GROUP BY c.customer_unique_id
HAVING COUNT(DISTINCT o.order_id)>1
ORDER BY orders DESC LIMIT 10;
