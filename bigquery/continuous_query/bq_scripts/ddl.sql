-- create dataset called real_time
----------------------------------------------------------------
CREATE TABLE `real_time.instrument_data` (
    instrument_id STRING NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    temperature FLOAT64,
    pressure FLOAT64,
    humidity FLOAT64
);

CREATE TABLE `real_time.instrument_data_processed` (
    instrument_id STRING NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    persistence_timestamp TIMESTAMP  DEFAULT CURRENT_TIMESTAMP(),
    temperature_F FLOAT64,
    pressure FLOAT64,
    humidity FLOAT64
);
