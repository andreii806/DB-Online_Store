DROP PROCEDURE IF EXISTS create_order;
-- PROC_END

CREATE PROCEDURE create_order(IN p_user_id INT, IN p_items_json JSON)
BEGIN
    DECLARE v_order_id INT;
    DECLARE v_i INT DEFAULT 0;
    DECLARE v_len INT DEFAULT 0;
    DECLARE v_sku VARCHAR(50);
    DECLARE v_qty INT;
    DECLARE v_product_id INT;

    INSERT INTO orders(user_id) VALUES (p_user_id);
    SET v_order_id = LAST_INSERT_ID();

    SET v_len = JSON_LENGTH(p_items_json);

    WHILE v_i < v_len DO
        SET v_sku = JSON_UNQUOTE(JSON_EXTRACT(p_items_json, CONCAT('$[', v_i, '].sku')));
        SET v_qty = JSON_EXTRACT(p_items_json, CONCAT('$[', v_i, '].qty'));

        SELECT id INTO v_product_id FROM products WHERE sku = v_sku LIMIT 1;

        INSERT INTO order_items(order_id, product_id, qty)
        VALUES (v_order_id, v_product_id, v_qty);

        SET v_i = v_i + 1;
    END WHILE;

    SELECT v_order_id AS order_id;
END
-- PROC_END