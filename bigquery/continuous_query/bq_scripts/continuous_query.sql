-- set the query options to Continuous 
INSERT INTO real_time.instrument_data_processed
(
  instrument_id, event_timestamp, 
  temperature_F, pressure, humidity
)
SELECT instrument_id,
TIMESTAMP AS event_timestamp,
ROUND(temperature*1.8 - 32, 2) as temperature_F, 
pressure,
humidity
FROM real_time.instrument_data;