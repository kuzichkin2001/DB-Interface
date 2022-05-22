CREATE OR REPLACE PROCEDURE GetReceiptForOffer(
    id_of_offer INT
)
LANGUAGE plpgsql AS $$
BEGIN
    DECLARE receipt TABLE 
    receipt := SELECT * FROM offer o WHERE offer_id = $offer_id
               RIGHT JOIN client c ON o.client_id = c.client_id

    SELECT * FROM receipt
END;$$;