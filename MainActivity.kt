////package com.example.hesapanalizi.ui.theme
//package com.example.hesapanalizi
//
//
//import android.os.Bundle
//import androidx.activity.ComponentActivity
//import androidx.activity.compose.setContent
//import androidx.activity.enableEdgeToEdge
//import androidx.compose.foundation.layout.*
//import androidx.compose.material3.*
//import androidx.compose.runtime.Composable
//import androidx.compose.ui.Modifier
//import androidx.compose.ui.tooling.preview.Preview
//import androidx.compose.ui.unit.dp
//import com.example.hesapanalizi.ui.theme.HesapanaliziTheme
//
//class MainActivity : ComponentActivity() {
//
//override fun onCreate(savedInstanceState: Bundle?) {
//    super.onCreate(savedInstanceState)
//    enableEdgeToEdge()
//    setContent {
//        HesapanaliziTheme {
//            MyApp()
//        }
//    }
//
//
//}
//
//
//
//
//
//
//
//
//    @OptIn(ExperimentalMaterial3Api::class)
////@OptIn(ExperimentalMaterial3Api::class)
//    @Composable
//    fun MyApp() {
//        Scaffold(
//            topBar = {
//                TopAppBar(
//                    title = { Text("Finans Uygulaması") }
//                )
//            },
//            content = { innerPadding ->
//                Box(modifier = Modifier.padding(innerPadding).fillMaxSize()) {
//                    MainScreen()
//                }
//            }
//        )
//    }
//@Composable
//fun MainScreen() {
//    Column(
//        modifier = Modifier
//            .fillMaxSize()
//            .padding(16.dp)
//    ) {
//        Text(text = "Merhaba!", style = MaterialTheme.typography.headlineSmall)
//        Spacer(modifier = Modifier.height(8.dp))
//        Text(text = "Bütçeni takip etmeye hazır mısın?")
//    }
//}
//@Preview(showBackground = true)
//@Composable
//fun MainScreenPreview() {
//    HesapanaliziTheme { MyApp() } }}
//


package com.example.hesapanalizi

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var editAmount: EditText
    private lateinit var radioGroup: RadioGroup
    private lateinit var radioIncome: RadioButton
    private lateinit var radioExpense: RadioButton
    private lateinit var btnAdd: Button
    private lateinit var listView: ListView
    private lateinit var totalView: TextView

    private val transactions = mutableListOf<String>()
    private lateinit var adapter: ArrayAdapter<String>
    private var totalAmount = 0 // Net tutar: gelir-gider farkı

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // XML'deki view'ları bağladık
        editAmount = findViewById(R.id.editAmount)
        radioGroup = findViewById(R.id.radioGroup)
        radioIncome = findViewById(R.id.radioIncome)
        radioExpense = findViewById(R.id.radioExpense)
        btnAdd = findViewById(R.id.btnAdd)
        listView = findViewById(R.id.listView)
        totalView = findViewById(R.id.totalView)

        adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, transactions)
        listView.adapter = adapter

        btnAdd.setOnClickListener {
            val amountText = editAmount.text.toString()
            val amount = amountText.toIntOrNull()

            if (amount == null || amount <= 0) {
                Toast.makeText(this, "Lütfen geçerli bir tutar girin", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val type = if (radioIncome.isChecked) "Gelir" else "Gider"
            val entry = "$type: $amount ₺"

            // AlertDialog gösterdik
            AlertDialog.Builder(this)
                .setTitle("İşlem Eklensin mi?")
                .setMessage(entry)
                .setPositiveButton("Evet") { _, _ ->
                    transactions.add(entry)
                    adapter.notifyDataSetChanged()

                    if (type == "Gelir") totalAmount += amount else totalAmount -= amount
                    totalView.text = "Toplam: $totalAmount ₺"
                    editAmount.text.clear()
                }
                .setNegativeButton("İptal", null)
                .show()
        }
    }
}













