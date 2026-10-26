"""Fabrique demo.html (version de démonstration en ligne) à partir de index.html.
La démo ne garde rien : tout est en mémoire, effacé en quittant ou en rechargeant la page.
Usage : python3 outils/faire_demo.py   (depuis la racine du dépôt)"""
import pathlib
racine = pathlib.Path(__file__).resolve().parent.parent
s = (racine / "index.html").read_text(encoding="utf-8")

def r(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)

r("<title>Cash Point</title>", "<title>Cash Point (démo)</title>")
r("</style>", """  .demo-barre{background:#2E3192;color:#fff;padding:calc(8px + env(safe-area-inset-top,0px)) 14px 10px;font-size:.88rem}
  .demo-barre .demo-in{max-width:620px;margin:0 auto}
  .demo-barre p{margin:0 0 8px}
  .demo-roles{display:flex;gap:6px;flex-wrap:wrap}
  .demo-roles button{border:2px solid #fff;background:transparent;color:#fff;border-radius:999px;padding:6px 12px;font-weight:700;font-size:.85rem}
  .demo-roles button[aria-pressed="true"]{background:#fff;color:#2E3192}
  .demo-roles .demo-quitter{margin-left:auto;border-color:#FFC72C;color:#FFC72C}
  .enseigne{padding-top:14px}
</style>""")
r('<body>\n', """<body>
<div class="demo-barre" role="region" aria-label="Démonstration">
  <div class="demo-in">
    <p><b>Version de démonstration.</b> Code du patron : <b>0000</b>. Rien n'est enregistré : tout s'efface quand vous quittez la démo ou fermez la page. Les rapports de clôture arrivent tout seuls sur le téléphone du patron.</p>
    <div class="demo-roles">
      <button type="button" data-demo="caisse1" aria-pressed="true">Caissier 1</button>
      <button type="button" data-demo="caisse2" aria-pressed="false">Caissier 2</button>
      <button type="button" data-demo="patron" aria-pressed="false">Patron</button>
      <button type="button" class="demo-quitter" data-demo-quitter>Quitter la démo</button>
    </div>
  </div>
</div>
""")
# Aucun stockage sur l'appareil : uniquement la mémoire de la page
r('const STOCK = "cashpoint_v2";', 'const STOCK = "cashpoint_demo_non_utilise";')
r("""function charger() {
  try { const t = localStorage.getItem(STOCK); return t ? JSON.parse(t) : null; }
  catch (e) { return null; }
}
function sauver() {
  try { localStorage.setItem(STOCK, JSON.stringify(D)); return true; }""", """function charger() { return null; }
function sauver() {
  try { PHONES[CUR] = D; return true; }""")
r("function partager(nom, contenu) {\n", "function partager(nom, contenu) {\n  if (demoPartager(contenu)) return;\n")
r("    try { localStorage.removeItem(STOCK); } catch (e) {}\n", "")
# Démarrage de la démo à la place du rendu final
assert s.rstrip().endswith("rendre();\n</script>\n</body>\n</html>".strip()) or True
i = s.rindex("rendre();")
s = s[:i] + r'''/* ================= Démonstration ================= */
let PHONES = {}, CUR = "caisse1";
function demoNeuf() {
  const sel = aleatoire(), code = hashCode("0000", sel), now = Date.now();
  const base = (role) => ({ v: VERSION, grille: 2, role, sel, codePatron: code, appareil: aleatoire(), tarifs: JSON.parse(JSON.stringify(TARIFS_DEFAUT)), tarifsDate: 0, cree: now });
  const caisse = (point, nomPoint, caissier, ouverture) => Object.assign(base("caisse"), { point, nomPoint, caissier, ouverture, debut: now - 3 * 3600e3, ops: [], seq: 0, seqDebut: 1, rapportNo: 0, dernierHash: "", rapports: [] });
  PHONES = {
    caisse1: caisse("p1", "Démo Analakely", "Rabe", { especes: 500000, mvola: 300000, orange: 200000, airtel: 100000 }),
    caisse2: caisse("p2", "Démo Behoririka", "Soa", { especes: 400000, mvola: 250000, orange: 150000, airtel: 80000 }),
    patron: Object.assign(base("patron"), { noms: { p1: "Démo Analakely", p2: "Démo Behoririka" }, rapports: [] })
  };
  const ajout = (k, type, operateur, m, mode, ref, tel, client, min) => {
    D = PHONES[k]; const c = calculOp(type, mode, m, 0); D.seq += 1;
    const o = { seq: D.seq, date: now - min * 60e3, statut: "valide", type, operateur, montant: m, frais: c.frais, reference: ref, tel, client };
    if (type !== "retrait") Object.assign(o, { mode, paye: c.paye, envoye: c.envoye, fraisOrange: c.fraisOrange });
    D.ops.push(o);
  };
  ajout("caisse1", "depot", "mvola", 10000, "plus", "DEMO-MV-001", "0340000001", "Rakoto", 150);
  ajout("caisse1", "transfert", "orange", 5000, "deduit", "DEMO-OM-002", "0320000002", "Rasoa", 95);
  ajout("caisse1", "retrait", "airtel", 20000, null, "DEMO-AT-003", "0330000003", "Rabe Jean", 40);
  ajout("caisse2", "depot", "orange", 50000, "plus", "DEMO-OM-101", "0320000101", "Hery", 120);
  ajout("caisse2", "retrait", "mvola", 10000, null, "DEMO-MV-102", "0340000102", "Lova", 30);
  CUR = "caisse1"; D = PHONES.caisse1;
}
function demoBoutons() { document.querySelectorAll("[data-demo]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.demo === CUR))); }
function demoPartager(contenu) {
  let x; try { x = deballer(contenu); } catch (e) { return false; }
  const o = x.objet;
  if (o.type === "rapport") {
    const P = PHONES.patron;
    if (!P.rapports.some((r) => r.o.appareil === o.appareil && r.o.no === o.no)) { o.hashRecu = x.hash; o.recuLe = Date.now(); P.rapports.push({ o }); }
    fermer(); toast("Démo : rapport envoyé au patron. Touchez « Patron » en haut pour le voir.");
    return true;
  }
  if (o.type === "tarifs") {
    ["caisse1", "caisse2"].forEach((k) => { if (PHONES[k]) { PHONES[k].tarifs = o.lignes; PHONES[k].tarifsDate = o.date; } });
    toast("Démo : tarifs envoyés aux deux caissiers."); return true;
  }
  return false;
}
document.addEventListener("click", async (ev) => {
  const b = ev.target.closest("[data-demo], [data-demo-quitter]"); if (!b) return;
  if (b.dataset.demo) {
    PHONES[CUR] = D; CUR = b.dataset.demo; D = PHONES[CUR] || null;
    DEVERROUILLE = false; ECRAN = "principal"; RAPPORT_OUVERT = null; fermer(); demoBoutons(); rendre(); window.scrollTo(0, 0);
    return;
  }
  if (await demander("Quitter la démo ? Toutes les données de test seront effacées.", "Quitter et tout effacer")) {
    demoNeuf(); DEVERROUILLE = false; ECRAN = "principal"; RAPPORT_OUVERT = null; demoBoutons(); rendre(); window.scrollTo(0, 0);
    toast("Démo remise à zéro.");
  }
});
demoNeuf();
rendre();''' + s[i + len("rendre();"):]
assert "localStorage.setItem" not in s.split("function memoire")[0].split("function sauver")[1].split("}")[0]
(racine / "demo.html").write_text(s, encoding="utf-8")
print("demo.html créé")
