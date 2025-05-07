package zws.database.models;

import sqlalchemy.Column;
import sqlalchemy.String;
import sqlalchemy.Integer;
import sqlalchemy.DateTime;
import sqlalchemy.ForeignKey;
import sqlalchemy.Index;
import zws.database.Base;
import zws.database.models.url_model.UrlModel;

public class VisitModel extends Base {
    public static final String __tablename__ = "visits";

    public static final Column<Integer> id = new Column<>(Integer.class, primaryKey = true, autoincrement = true);
    public static final Column<String> url_short_base64 = new Column<>(String.class, ForeignKey.class("url_model.short_base64"), notNull = true);
    public static final Column<DateTime> timestamp = new Column<>(DateTime.class, notNull = true);

    static {
        new Index("ix_visits_url_short_base64", url_short_base64);
    }
}