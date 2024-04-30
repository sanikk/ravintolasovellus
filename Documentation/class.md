
```mermaid
classDiagram
    class specialty {
        %% WIP
        +int specialty_id
        +restaurant_id restaurant_id
        +int category
        +text description
    }
    class event {
        %% admin rights for event_owner & restaurant_owner
        +int event_id
        +text event_name
        +restaurant_id venue_id
        +timestamp posted_on
        +account_id<int> event_owner
        +timestamp event_start
        +timestamp event_end
        +text repeat_interval
        +text description
    }
    class buffet {
        %% owner/admin through restaurant
        +int buffet_id
        +text buffet_name
        +restaurant_id venue_id
        +timestamp posted_on
        +timestamp buffet_start
        +timestamp buffet_end
        +text repeat_interval
        +int account_id
        +text description
        }
    class review {
        +int review_id
        +account_id poster_id
        +restaurant_id reviewed_restaurant_id
        +timestamp posted_on
        +int rating
        +text review_content
        }
    class restaurant {
        +int restaurant_id
        +text restaurant_name
        %% location
        +float latitude
        +float longitude
        %% google?
        +text place_id
        +text address
        +text description
        }
    class account {
        +int id
        +text username
        +text realname
        +text password
        +int role
        +text bio
        }
    specialty ..> restaurant : restaurant_id    
    review ..> account : account_id
    review ..> restaurant : restaurant_id
    buffet ..> account : account_id
    buffet ..> restaurant : restaurant_id
    event ..> account : account_id
    event ..> restaurant : restaurant_id
```