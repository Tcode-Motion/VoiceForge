import SwiftUI
import WebKit

/// VoiceForge companion for iOS.
/// The engines run on your computer; this app is the studio
/// interface: point it at VoiceForge on your PC (same Wi-Fi).
/// Styled to match the studio: near-black surfaces, one lime accent.
struct ContentView: View {
    @AppStorage("vf_url") private var urlText: String = ""
    @State private var loadedURL: URL?

    private let bg = Color(red: 0.039, green: 0.039, blue: 0.043)
    private let panel = Color(red: 0.063, green: 0.063, blue: 0.071)
    private let field = Color(red: 0.051, green: 0.051, blue: 0.059)
    private let lime = Color(red: 0.784, green: 0.961, blue: 0.259)
    private let dim = Color(red: 0.639, green: 0.639, blue: 0.671)

    var body: some View {
        VStack(spacing: 0) {
            VStack(alignment: .leading, spacing: 10) {
                HStack(spacing: 10) {
                    Image(systemName: "waveform")
                        .foregroundColor(lime)
                        .font(.title3)
                    VStack(alignment: .leading, spacing: 1) {
                        Text("VoiceForge")
                            .font(.headline)
                            .foregroundColor(.white)
                        Text("CPU Voice Cloning Studio")
                            .font(.caption)
                            .foregroundColor(dim)
                    }
                }
                HStack(spacing: 10) {
                    TextField("http://192.168.1.5:8760", text: $urlText)
                        .padding(10)
                        .background(field)
                        .cornerRadius(10)
                        .foregroundColor(.white)
                        .autocapitalization(.none)
                        .autocorrectionDisabled(true)
                        .keyboardType(.URL)
                    Button("Connect") {
                        var text = urlText.trimmingCharacters(in: .whitespaces)
                        if !text.hasPrefix("http") { text = "http://" + text }
                        loadedURL = URL(string: text)
                    }
                    .font(.subheadline.bold())
                    .padding(.horizontal, 16)
                    .padding(.vertical, 10)
                    .background(Color.white)
                    .foregroundColor(.black)
                    .cornerRadius(10)
                }
            }
            .padding(16)
            .background(panel)

            if let url = loadedURL {
                WebView(url: url)
            } else {
                Spacer()
                Image(systemName: "waveform.circle")
                    .font(.system(size: 44))
                    .foregroundColor(lime)
                    .padding(.bottom, 12)
                Text("Start VoiceForge on your computer with:\nvoiceforge gui\nthen connect here on the same Wi-Fi.")
                    .multilineTextAlignment(.center)
                    .foregroundColor(dim)
                    .font(.subheadline)
                    .padding(.horizontal, 32)
                Spacer()
            }
        }
        .background(bg.ignoresSafeArea())
        .preferredColorScheme(.dark)
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
