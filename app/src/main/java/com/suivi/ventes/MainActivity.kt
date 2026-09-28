package com.suivi.ventes

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import org.json.JSONObject
import java.io.File

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private var rappelFichier: ValueCallback<Array<Uri>>? = null

    // Choix d'un fichier reçu (rapport, tarifs, sauvegarde)
    private val choixFichier = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { res ->
        rappelFichier?.onReceiveValue(WebChromeClient.FileChooserParams.parseResult(res.resultCode, res.data))
        rappelFichier = null
    }

    // Pont appelé par l'application : window.Android.partager(nom, contenu)
    inner class Pont {
        @JavascriptInterface
        fun partager(nom: String, contenu: String) {
            runOnUiThread {
                try {
                    val dossier = File(cacheDir, "rapports")
                    dossier.mkdirs()
                    val propre = nom.replace(Regex("[^A-Za-z0-9._-]"), "_")
                    val fichier = File(dossier, propre)
                    fichier.writeText(contenu, Charsets.UTF_8)
                    val uri = FileProvider.getUriForFile(this@MainActivity, "$packageName.fichiers", fichier)
                    val envoi = Intent(Intent.ACTION_SEND).apply {
                        type = "text/plain"
                        putExtra(Intent.EXTRA_STREAM, uri)
                        putExtra(Intent.EXTRA_SUBJECT, propre)
                        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    }
                    startActivity(Intent.createChooser(envoi, "Envoyer avec…"))
                } catch (e: Exception) {
                    webView.evaluateJavascript("window.erreurAndroid && window.erreurAndroid(" + JSONObject.quote(e.message ?: "erreur") + ")", null)
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.webview)
        findViewById<SwipeRefreshLayout>(R.id.swipeRefresh).isEnabled = false

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = true
        webView.settings.setSupportZoom(false)

        webView.webViewClient = WebViewClient()
        webView.webChromeClient = object : WebChromeClient() {
            override fun onShowFileChooser(view: WebView?, callback: ValueCallback<Array<Uri>>?, params: FileChooserParams?): Boolean {
                rappelFichier?.onReceiveValue(null)
                rappelFichier = callback
                val intention = Intent(Intent.ACTION_GET_CONTENT).apply {
                    addCategory(Intent.CATEGORY_OPENABLE)
                    type = "*/*"
                }
                return try {
                    choixFichier.launch(Intent.createChooser(intention, "Choisir le fichier reçu"))
                    true
                } catch (e: Exception) {
                    rappelFichier = null
                    false
                }
            }
        }
        webView.addJavascriptInterface(Pont(), "Android")

        // L'application est dans l'APK : elle fonctionne sans internet.
        webView.loadUrl("file:///android_asset/index.html")
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        webView.evaluateJavascript("(window.retour && window.retour()) ? 'oui' : 'non'") { r ->
            if (r != "\"oui\"") finish()
        }
    }
}
