import { useState } from 'react'
import type { PipelineResponse } from '../api/pipeline/types'
import { PipelineResultSkeleton } from './PipelineResultSkeleton'

interface PipelineResultProps {
  result: PipelineResponse | null
  error: string | null
  loading?: boolean
}

export function PipelineResult({ result, error, loading = false }: PipelineResultProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async (text: string) => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  if (loading) {
    return <PipelineResultSkeleton />
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl border border-stone-200 shadow-sm p-8">
        <p className="text-red-700 font-medium">{error}</p>
      </div>
    )
  }

  if (!result) return null

  return (
    <div className="bg-white rounded-xl border border-stone-200 shadow-sm p-8">
      <div className="flex items-center gap-3">
        <span className="text-lg font-semibold text-stone-900">{result.company_domain}</span>
        <span
          className={
            result.is_qualified
              ? 'bg-orange-50 text-orange-900 border border-orange-100 rounded-full px-3 py-1 text-xs font-semibold'
              : 'bg-stone-100 text-stone-600 border border-stone-200 rounded-full px-3 py-1 text-xs font-semibold'
          }
        >
          {result.is_qualified ? 'Qualified' : 'Not qualified'}
        </span>
      </div>
      <p className="text-stone-600 text-sm mt-2 leading-relaxed">{result.reason}</p>

      {result.draft_email && (
        <div className="bg-stone-100 border border-stone-200 rounded-lg p-5 mt-6">
          <div className="flex justify-between items-center mb-3">
            <span className="text-[11px] font-bold tracking-wider text-stone-500 uppercase">Draft email</span>
            <button
              type="button"
              onClick={() => handleCopy(result.draft_email!)}
              className="text-xs font-medium text-stone-600 hover:text-stone-900 hover:bg-stone-200 px-3 py-1.5 rounded-md transition-colors"
            >
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>
          <pre className="text-stone-800 text-sm leading-relaxed whitespace-pre-wrap font-sans">
            {result.draft_email}
          </pre>
        </div>
      )}
    </div>
  )
}
