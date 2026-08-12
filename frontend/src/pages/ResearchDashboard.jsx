import { useState } from "react";
import { runResearch } from "../services/researchApi";

function ResearchDashboard() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleResearch = async () => {
    if (!question.trim() || loading) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await runResearch(question, 5);

      setResult(data);
    } catch (err) {
      setError(
        err.message || "Unable to complete research."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <div className="brand">MODUS</div>
          <div className="subtitle">
            Enterprise Research Intelligence
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          {loading ? "Researching..." : "System Ready"}
        </div>
      </header>

      <main className="dashboard">

        {/* HERO */}
        <section className="hero">
          <div className="eyebrow">
            AI RESEARCH AGENT
          </div>

          <h1>
            Turn documents into
            <span> evidence-backed intelligence.</span>
          </h1>

          <p>
            Ask a research question and MODUS will retrieve
            evidence, identify findings, compare sources,
            detect contradictions, and generate a conclusion.
          </p>
        </section>

        {/* RESEARCH INPUT */}
        <section className="research-box">
          <label>Research Question</label>

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            placeholder="Ask something about your uploaded documents..."
            rows={5}
            disabled={loading}
          />

          <div className="research-actions">
            <span>
              Evidence-based research
            </span>

            <button
              onClick={handleResearch}
              disabled={loading || !question.trim()}
            >
              {loading
                ? "Researching..."
                : "Run Research →"}
            </button>
          </div>
        </section>

        {/* ERROR */}
        {error && (
          <section className="result-section error-box">
            <div className="section-title">
              Research Error
            </div>

            <p>{error}</p>
          </section>
        )}

        {/* RESULT */}
        {result && (
          <section className="results">

            {/* ANSWER */}
            <div className="result-section">
              <div className="section-title">
                Research Answer
              </div>

              <div className="answer-card">
                <p>{result.answer}</p>
              </div>
            </div>

            {/* CONCLUSION */}
            {result.conclusion && (
              <div className="result-section">
                <div className="section-title">
                  Final Conclusion
                </div>

                <div className="conclusion-card">
                  <div className="confidence">
                    Confidence:{" "}
                    <strong>
                      {result.conclusion.confidence}
                    </strong>
                  </div>

                  <h2>
                    {result.conclusion.conclusion}
                  </h2>

                  {result.conclusion.key_takeaways
                    ?.length > 0 && (
                    <>
                      <h3>Key Takeaways</h3>

                      <ul>
                        {result.conclusion.key_takeaways.map(
                          (item, index) => (
                            <li key={index}>
                              {item}
                            </li>
                          )
                        )}
                      </ul>
                    </>
                  )}

                  {result.conclusion.caveats
                    ?.length > 0 && (
                    <>
                      <h3>Caveats</h3>

                      <ul>
                        {result.conclusion.caveats.map(
                          (item, index) => (
                            <li key={index}>
                              {item}
                            </li>
                          )
                        )}
                      </ul>
                    </>
                  )}
                </div>
              </div>
            )}

            {/* FINDINGS */}
            {result.findings && (
              <div className="result-section">
                <div className="section-title">
                  Research Findings
                </div>

                <div className="findings-grid">
                  {Array.isArray(result.findings)
                    ? result.findings.map(
                        (finding, index) => (
                          <div
                            className="finding-card"
                            key={index}
                          >
                            <div className="card-number">
                              Finding {index + 1}
                            </div>

                            <h3>
                              {finding.claim ||
                                finding.title ||
                                "Research Finding"}
                            </h3>

                            <p>
                              {finding.evidence ||
                                finding.description ||
                                ""}
                            </p>
                          </div>
                        )
                      )
                    : (
                      <div className="finding-card">
                        <pre>
                          {JSON.stringify(
                            result.findings,
                            null,
                            2
                          )}
                        </pre>
                      </div>
                    )}
                </div>
              </div>
            )}

            {/* EVIDENCE */}
            {result.evidence?.length > 0 && (
              <div className="result-section">
                <div className="section-title">
                  Evidence Traceability
                </div>

                <div className="evidence-list">
                  {result.evidence.map(
                    (item, index) => (
                      <div
                        className="evidence-card"
                        key={index}
                      >
                        <div className="evidence-header">
                          <span>
                            Evidence {index + 1}
                          </span>

                          <span>
                            Source #{item.source_index}
                          </span>
                        </div>

                        <h3>
                          {item.claim}
                        </h3>

                        <p>
                          {item.evidence}
                        </p>

                        <div className="source-meta">
                          <strong>Source</strong>

                          <pre>
                            {JSON.stringify(
                              item.source?.metadata ||
                                {},
                              null,
                              2
                            )}
                          </pre>
                        </div>
                      </div>
                    )
                  )}
                </div>
              </div>
            )}

            {/* COMPARISON */}
            {result.comparison && (
              <div className="result-section">
                <div className="section-title">
                  Evidence Comparison
                </div>

                <div className="comparison-grid">

                  <div className="comparison-card">
                    <h3>Agreements</h3>

                    {result.comparison.agreements
                      ?.length > 0 ? (
                      <ul>
                        {result.comparison.agreements.map(
                          (item, index) => (
                            <li key={index}>
                              {item}
                            </li>
                          )
                        )}
                      </ul>
                    ) : (
                      <p>No agreements identified.</p>
                    )}
                  </div>

                  <div className="comparison-card">
                    <h3>Disagreements</h3>

                    {result.comparison.disagreements
                      ?.length > 0 ? (
                      <ul>
                        {result.comparison.disagreements.map(
                          (item, index) => (
                            <li key={index}>
                              {item}
                            </li>
                          )
                        )}
                      </ul>
                    ) : (
                      <p>No disagreements identified.</p>
                    )}
                  </div>

                </div>

                {/* CONTRADICTIONS */}
                {result.comparison.contradictions
                  ?.length > 0 && (
                  <div className="contradictions">
                    <h3>
                      ⚠ Contradictions
                    </h3>

                    {result.comparison.contradictions.map(
                      (item, index) => (
                        <div
                          className="contradiction-card"
                          key={index}
                        >
                          <strong>
                            Contradiction {index + 1}
                          </strong>

                          <p>
                            <b>Claim A:</b>{" "}
                            {item.claim_a}
                          </p>

                          <p>
                            <b>Claim B:</b>{" "}
                            {item.claim_b}
                          </p>

                          <p>
                            <b>Explanation:</b>{" "}
                            {item.explanation}
                          </p>
                        </div>
                      )
                    )}
                  </div>
                )}
              </div>
            )}

            {/* SOURCES */}
            {result.sources?.length > 0 && (
              <div className="result-section">
                <div className="section-title">
                  Sources
                </div>

                <div className="sources-list">
                  {result.sources.map(
                    (source, index) => (
                      <div
                        className="source-card"
                        key={index}
                      >
                        <div className="source-number">
                          Source {index + 1}
                        </div>

                        <p>
                          {source.document}
                        </p>

                        <small>
                          Hybrid Score:{" "}
                          {source.hybrid_score !==
                          null &&
                          source.hybrid_score !==
                          undefined
                            ? source.hybrid_score.toFixed(
                                3
                              )
                            : "N/A"}
                        </small>
                      </div>
                    )
                  )}
                </div>
              </div>
            )}

          </section>
        )}

        {/* PIPELINE */}
        {!result && !loading && (
          <section className="pipeline">

            <div className="section-title">
              Research Pipeline
            </div>

            <div className="pipeline-grid">

              <div className="pipeline-card">
                <div className="number">01</div>
                <h3>Retrieve</h3>
                <p>
                  Hybrid semantic and keyword retrieval.
                </p>
              </div>

              <div className="pipeline-card">
                <div className="number">02</div>
                <h3>Findings</h3>
                <p>
                  Extract structured research claims.
                </p>
              </div>

              <div className="pipeline-card">
                <div className="number">03</div>
                <h3>Evidence</h3>
                <p>
                  Trace every finding back to its source.
                </p>
              </div>

              <div className="pipeline-card">
                <div className="number">04</div>
                <h3>Compare</h3>
                <p>
                  Identify agreements and contradictions.
                </p>
              </div>

              <div className="pipeline-card">
                <div className="number">05</div>
                <h3>Synthesize</h3>
                <p>
                  Generate an evidence-based conclusion.
                </p>
              </div>

            </div>
          </section>
        )}

      </main>
    </div>
  );
}

export default ResearchDashboard;