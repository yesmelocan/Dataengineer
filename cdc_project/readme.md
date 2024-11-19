-- DB name postgres
CREATE TABLE IF NOT EXISTS user_activity (
    UserID VARCHAR(10),
    SessionID VARCHAR(10),
    Timestamp TIMESTAMP,
    Page_URL VARCHAR(255),
    Action VARCHAR(50),
    Referrer_URL VARCHAR(255),
    Device VARCHAR(20),
    Browser VARCHAR(20)
);

INSERT INTO user_activity (UserID, SessionID, Timestamp, Page_URL, Action, Referrer_URL, Device, Browser) VALUES 
('001', 'abc123', '2024-10-23 10:15:23', '/home', 'Page View', NULL, 'Desktop', 'Chrome'),
('001', 'abc123', '2024-10-23 10:16:10', '/product/123', 'Page View', '/home', 'Desktop', 'Chrome'),
('001', 'abc123', '2024-10-23 10:17:45', '/cart', 'Add to Cart', '/product/123', 'Desktop', 'Chrome'),
('002', 'xyz789', '2024-10-23 10:19:02', '/login', 'Login', NULL, 'Mobile', 'Safari'),
('002', 'xyz789', '2024-10-23 10:20:12', '/product/456', 'Page View', '/home', 'Mobile', 'Safari'),
('002', 'xyz789', '2024-10-23 10:22:30', '/checkout', 'Checkout Start', '/cart', 'Mobile', 'Safari');



  curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://34.136.76.36:8083/connectors/ -d @register-postgres.json

  curl -X PUT http://localhost:8083/connectors/postgres-connector/pause
  curl -X DELETE http://localhost:8083/connectors/postgres-connector  

  curl -X PUT http://34.136.76.36:8083/connectors/postgres-connector/pause
  curl -X PUT http://34.136.76.36:8083/connectors/postgres-connector/resume

  curl -X DELETE http://34.136.76.36:8083/connectors/postgres-connector

  kafka-topics.sh --describe --topic <topic_adı> --bootstrap-server <broker_adresi>

  curl -X GET http://34.136.76.36:8083/connectors/postgres-connector/status


INSERT INTO turnstile_activity (employee_id, timestamp, entry_exit, location, device_id, access_type) VALUES
('E001', '2024-11-01 08:30:00', 'entry333', 'Main Entrance', 'T001', 'employee'),
('E004', '2024-11-01 09:15:00', 'entry', 'Main Entrance', 'T001', 'employee'),
('E002', '2024-11-01 12:30:00', 'exit', 'Main Entrance', 'T001', 'employee'),
('E003', '2024-11-01 17:30:00', 'exit', 'Side Entrance', 'T002', 'visitor'),
('E005', '2024-11-01 08:00:00', 'entry', 'Main Entrance', 'T001', 'contractor'),
('E005', '2024-11-01 16:00:00', 'exit', 'Main Entrance', 'T001', 'contractor');


























,
--('E002', '2024-11-01 08:45:00', 'entry', 'Main Entrance', 'T001', 'employee') ,
--('E001', '2024-11-01 17:00:00', 'exit', 'Main Entrance', 'T001', 'employee'),
--('E003', '2024-11-01 09:00:00', 'entry', 'Side Entrance', 'T002', 'visitor'),



ALTER PUBLICATION dbz_publication ADD TABLE public.turnstile_activity;

--select * from  turnstile_activity
select * from public.turnstile_activity

select * from turnstile_activity
--ALTER TABLE user_activity REPLICA IDENTITY FULL;

SELECT * FROM pg_replication_slots;
SELECT * FROM pg_publication;
SELECT * FROM pg_replication_slots;


SELECT pg_drop_replication_slot('debezium');
SELECT * FROM pg_publication_tables WHERE pubname = 'dbz_publication';


UPDATE turnstile_activity
SET timestamp = '2024-11-01 08:30:00'
WHERE timestamp = '2024-11-01 08:42:00';







CREATE TABLE IF NOT EXISTS turnstile_activity (
    employee_id VARCHAR(10),
    timestamp TIMESTAMP,
    entry_exit VARCHAR(10),  -- 'entry' or 'exit'
    location VARCHAR(100),
    device_id VARCHAR(10),    -- ID of the turnstile or device
    access_type VARCHAR(20)    -- e.g., 'employee', 'visitor', etc.
);
