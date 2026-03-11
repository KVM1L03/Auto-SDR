import type { PipelineResponse } from '../api/pipeline/types'

interface PipelineResultProps {
  result: PipelineResponse | null
  error: string | null
}

export function PipelineResult({ result, error }: PipelineResultProps) {
  if (error) {
    return (
      <div className="mt-6 p-4 w-full max-w-md rounded-lg bg-red-900/50 border border-red-700 text-red-200">
        {error}
      </div>
    )
  }

  if (!result) return null

  return (
    <div className="mt-6 p-4 w-full max-w-md rounded-lg bg-slate-800 border border-slate-600 text-left">
      <div className="flex items-center gap-2 mb-2">
        <span className="font-medium text-white">{result.company_domain}</span>
        <span
          className={`px-2 py-0.5 rounded text-sm font-medium ${
            result.is_qualified ? 'bg-green-900/50 text-green-300' : 'bg-red-900/50 text-red-300'
          }`}
        >
          {result.is_qualified ? 'Qualified' : 'Not qualified'}
        </span>
      </div>
      <p className="text-slate-300 text-sm mb-3">{result.reason}</p>
      {result.draft_email && (
        <div className="pt-3 border-t border-slate-600">
          <p className="text-slate-400 text-xs mb-1">Draft email:</p>
          <pre className="text-slate-300 text-sm whitespace-pre-wrap font-sans">
            {result.draft_email}
          </pre>
        </div>
      )}
    </div>
  )
}
