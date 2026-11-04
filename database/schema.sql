CREATE TABLE IF NOT EXISTS "product" (
	"id" INTEGER NOT NULL,
	"label" VARCHAR NOT NULL,
	"sku" VARCHAR NOT NULL UNIQUE,
	"category" INTEGER NOT NULL,
	"sale_price" INTEGER NOT NULL CHECK ("sale_price" >= 0),
	"is_active" BOOLEAN NOT NULL DEFAULT 1 CHECK ("is_active" IN (0, 1)),
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "supplier" (
	"id" INTEGER NOT NULL,
	"name" VARCHAR NOT NULL,
	"email" VARCHAR NOT NULL,
	"phone" VARCHAR NOT NULL,
	"mean_time" INTEGER CHECK ("mean_time" IS NULL OR "mean_time" >= 0),
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "stocks" (
	"id" INTEGER NOT NULL,
	"id_product" INTEGER NOT NULL UNIQUE,
	"store_count" INTEGER NOT NULL DEFAULT 0 CHECK ("store_count" >= 0),
	"reserve_count" INTEGER NOT NULL DEFAULT 0 CHECK ("reserve_count" >= 0),
	PRIMARY KEY("id"),
	FOREIGN KEY ("id_product") REFERENCES "product"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "movements" (
	"id" INTEGER NOT NULL,
	"id_stock" INTEGER NOT NULL,
	"stock_before" INTEGER NOT NULL CHECK ("stock_before" >= 0),
	"stock_after" INTEGER NOT NULL CHECK ("stock_after" >= 0),
	"quantity_moves" INTEGER NOT NULL CHECK ("quantity_moves" != 0),
	"type_movement" INTEGER NOT NULL CHECK ("type_movement" IN (1, 2, 3)),
	"date_move" INTEGER NOT NULL,
	"is_reserve" BOOLEAN NOT NULL CHECK ("is_reserve" IN (0, 1)),
	PRIMARY KEY("id"),
	FOREIGN KEY ("id_stock") REFERENCES "stocks"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "ck_stock_after_coherent"
	CHECK ("stock_after" = "stock_before" + "quantity_moves")
);

CREATE TABLE IF NOT EXISTS "supplier_product" (
	"id" INTEGER NOT NULL,
	"id_product" INTEGER NOT NULL,
	"id_supplier" INTEGER NOT NULL,
	"purchase_price" INTEGER NOT NULL CHECK ("purchase_price" >= 0),
	PRIMARY KEY("id"),
	FOREIGN KEY ("id_product") REFERENCES "product"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("id_supplier") REFERENCES "supplier"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "uq_product_supplier" UNIQUE ("id_product", "id_supplier")
);

CREATE TABLE IF NOT EXISTS "alert" (
	"id" INTEGER NOT NULL,
	"id_stock" INTEGER NOT NULL UNIQUE,
	"threshold" INTEGER NOT NULL CHECK ("threshold" >= 0),
	PRIMARY KEY("id"),
	FOREIGN KEY ("id_stock") REFERENCES "stocks"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);