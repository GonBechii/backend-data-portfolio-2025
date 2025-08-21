```mermaid
erDiagram
  CUSTOMER ||--o{ ORDER : places }
  ORDER ||--|{ ORDER_ITEM : contains }
  PRODUCT ||--o{ ORDER_ITEM : appears_in }

  CUSTOMER {
    int id PK
    string name
    string email
    string phone
    datetime created_at
  } 
  
  ORDER {
    int id PK
    int customer_id FK
    string status
    decimal subtotal
    decimal total
    datetime created_at
    datetime updated_at
  }

  ORDER_ITEM {
    int id PK
    int order_id FK
    int product_id FK
    int quantity
    decimal unit_price
    decimal line_total
  }

  PRODUCT {
    int id PK
    string sku
    string name
    decimal price
    int stock
  }