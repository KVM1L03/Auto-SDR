import { useState } from 'react'
import type { SubmitEventHandler } from 'react'
import { runPipeline } from './api/pipeline'
import type { PipelineResponse } from './api/pipeline/types'
import { PipelineResult } from './components/PipelineResult'

function App() {
  const [domain, setDomain] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PipelineResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit: SubmitEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault()
    if (!domain.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await runPipeline(domain.trim())
      setResult(data)
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'An error occurred while analyzing the lead'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-stone-50">
      <div className="flex flex-col gap-6 max-w-xl w-full mx-auto mt-12 px-8">
        <div className="bg-white rounded-xl border border-stone-200 shadow-sm p-8">
          <h1 className="text-2xl font-bold text-stone-900 mb-6">
            Auto-SDR
          </h1>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              placeholder="Enter company domain (e.g. example.com)"
              disabled={loading}
              className="w-full py-3 px-4 rounded-lg border border-stone-300 text-stone-800 placeholder-stone-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-orange-600 hover:bg-orange-700 text-white font-medium rounded-lg transition-colors mt-4 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-orange-600"
            >
              {loading ? 'Analyzing...' : 'Analyze Lead'}
            </button>
          </form>
        </div>

        <PipelineResult result={result} error={error} loading={loading} />
      </div>
    </div>
  )
}

export default App
