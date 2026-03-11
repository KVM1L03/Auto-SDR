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
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center p-8">
      <h1 className="text-2xl font-bold text-white mb-8">
        Auto-SDR
      </h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-md">
        <input
          type="text"
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
          placeholder="Domain name"
          disabled={loading}
          className="px-4 py-3 rounded-lg border border-slate-600 bg-slate-800 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors"
        >
          {loading ? 'Analyzing...' : 'Analyze Lead'}
        </button>
      </form>

      <PipelineResult result={result} error={error} />
    </div>
  )
}

export default App
