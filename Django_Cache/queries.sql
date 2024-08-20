SELECT "shopapp_product"."id",
 "shopapp_product"."name",
 "shopapp_product"."description",
   "shopapp_product"."price",
    "shopapp_product"."discount",
     "shopapp_product"."created_at",
      "shopapp_product"."archived",
       "shopapp_product"."created_by_id",
        "shopapp_product"."preview" FROM "shopapp_product" WHERE NOT "shopapp_product"."archived" ORDER BY "shopapp_product"."name" ASC, "shopapp_product"."price" ASC;
SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."id" = 33 LIMIT 21;
