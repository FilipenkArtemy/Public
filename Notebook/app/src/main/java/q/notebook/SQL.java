package q.notebook;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

public class SQL extends SQLiteOpenHelper {

    private static final String DB_NAME = "SQL.db";
    private static final int DB_VERSION = 1;
    private static final String DB_TABLE = "note";

    public static final String COLUMN_ID = "_id";
    public static final String COLUMN_SM = "summary";
    public static final String COLUMN_DES = "description";

    private static final String DB_CREATE = "create table "
            + DB_TABLE + "(" + COLUMN_ID
            + " integer primary key autoincrement, " + COLUMN_SM + " text not null,"
            + COLUMN_DES + " text not null" + ");";

    public SQL(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(DB_CREATE);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS SQL");
        onCreate(db);
    }


    public long createSQL(String head,
                              String description) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues initialValues = createContentValues(head,
                description);

        long row = db.insert(DB_TABLE, null, initialValues);
        db.close();

        return row;
    }


    public boolean updateSQL(long rowId,  String head,
                              String description) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues updateValues = createContentValues(head,
                description);

        return db.update(DB_TABLE, updateValues, COLUMN_ID + "=" + rowId,
                null) > 0;
    }

    public void deleteSQL(long rowId) {
        SQLiteDatabase db = this.getWritableDatabase();
        db.delete(DB_TABLE, COLUMN_ID + "=" + rowId, null);
        db.close();
    }

    public Cursor getAlldata() {
        SQLiteDatabase db = this.getWritableDatabase();
        return db.query(DB_TABLE, new String[] { COLUMN_ID, COLUMN_SM, COLUMN_DES }, null,
                null, null, null, null);
    }


    public Cursor getSQL(long rowId) throws SQLException {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor mCursor = db.query(true, DB_TABLE,
                new String[] { COLUMN_ID, COLUMN_SM,
                        COLUMN_DES }, COLUMN_ID + "=" + rowId, null,
                null, null, null, null);
        if (mCursor != null) {
            mCursor.moveToFirst();
        }
        return mCursor;
    }

    private ContentValues createContentValues(String head,
                                              String description) {
        ContentValues values = new ContentValues();
        values.put(COLUMN_SM, head);
        values.put(COLUMN_DES, description);
        return values;
    }
}