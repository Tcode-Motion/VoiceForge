import SwiftUI
import WebKit

/// VoiceForge companion for iOS.
/// The engines run on your computer; this app is the studio
/// interface: point it at VoiceForge on your PC (same Wi-Fi).
struct ContentView: View {
    @AppStorage("vf_url") private var urlText: String = ""
    @State private var loadedURL: URL?

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                TextField("http://192.168.1.5:8760", text: $urlText)
                    .textFieldStyle(.roundedBorder)
                    .autocapitalization(.none)
                    .keyboardType(.URL)
                Button("Connect") {
                    var text = urlText.trimmingCharacters(in: .whitespaces)
                    if !text.hasPrefix("http") { text = "http://" + text }
                    loadedURL = URL(string: text)
                }
                .buttonStyle(.borderedProminent)
            }
            .padding(10)

            if let url = loadedURL {
                WebView(url: url)
            } else {
                Spacer()
                Text("Start VoiceForge on your computer with:\nvoiceforge gui\nthen connect here.")
                    .multilineTextAlignment(.center)
                    .foregroundColor(.secondary)
                    .padding()
                Spacer()
            }
        }
        .onAppear {
            if !urlText.isEmpty {
                loadedURL = URL(string: urlText)
            }
        }
    }
}

struct WebView: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        let view = WKWebView(frame: .zero, configuration: config)
        view.load(URLRequest(url: url))
        return view
    }

    func updateUIView(_ view: WKWebView, context: Context) {
        if view.url != url {
            view.load(URLRequest(url: url))
        }
    }
}
