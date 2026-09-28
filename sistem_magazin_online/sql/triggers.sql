DROP TRIGGER IF EXISTS trg_inventory_before_insert;
-- TRIGGER_END

CREATE TRIGGER trg_inventory_before_insert
BEFORE INSERT ON inventory_moves
FOR EACH ROW
BEGIN
    IF NEW.qty <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cantitatea trebuie sa fie mai mare decat 0';
    END IF;
END;
-- TRIGGER_END


DROP TRIGGER IF EXISTS trg_products_after_update;
-- TRIGGER_END

CREATE TRIGGER trg_products_after_update
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    INSERT INTO user_log (user_id, action)
    VALUES (user_id_1, CONCAT('UPDATE PRODUS ', OLD.sku));
END;
-- TRIGGER_END
