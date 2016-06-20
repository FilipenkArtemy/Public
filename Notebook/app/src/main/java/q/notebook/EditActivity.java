package q.notebook;

import android.os.Bundle;
import android.app.Activity;
import android.database.Cursor;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

public class EditActivity extends Activity {

    private EditText mTitleText;
    private EditText mBodyText;
    private Long mRowId;
    private SQL mDbHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mDbHelper = new SQL(this);

        setContentView(R.layout.activity_edit);

        mTitleText = (EditText) findViewById(R.id.note_edit_head);
        mBodyText = (EditText) findViewById(R.id.note_edit_description);

        Button confirmButton = (Button) findViewById(R.id.note_edit_button);
        mRowId = null;
        Bundle extras = getIntent().getExtras();

        mRowId = (savedInstanceState == null) ? null
                : (Long) savedInstanceState
                .getSerializable(SQL.COLUMN_ID);
        if (extras != null) {
            mRowId = extras.getLong(SQL.COLUMN_ID);
        }

        confirmButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                if (TextUtils.isEmpty(mTitleText.getText().toString())) {
                    Toast.makeText(EditActivity.this, "Данные не введены",
                            Toast.LENGTH_LONG).show();
                } else {
                    saveState();
                    setResult(RESULT_OK);
                    finish();
                }
            }
        });
    }

    private void populateFields() {
        if (mRowId != null) {
            Cursor note = mDbHelper.getSQL(mRowId);

            mTitleText.setText(note.getString(note
                    .getColumnIndexOrThrow(SQL.COLUMN_SM)));
            mBodyText.setText(note.getString(note
                    .getColumnIndexOrThrow(SQL.COLUMN_DES)));
        }
    }


    @Override
    protected void onResume() {
        super.onResume();
        populateFields();
    }

    private void saveState() {
        String summary = mTitleText.getText().toString();
        String description = mBodyText.getText().toString();

        if (description.length() == 0 && summary.length() == 0) {
            return;
        }

        if (mRowId == null) {
            long id = mDbHelper.createSQL(summary, description);
            if (id > 0) {
                mRowId = id;
            }
        } else {
            mDbHelper.updateSQL(mRowId, summary, description);
        }
    }
}