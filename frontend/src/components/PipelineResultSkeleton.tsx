function SkeletonLine({ className = '' }: { className?: string }) {
  return (
    <div
      className={`h-4 rounded bg-stone-200 animate-pulse ${className}`}
      aria-hidden
    />
  )
}

export function PipelineResultSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-stone-200 shadow-sm p-8">
      <div className="flex items-center gap-3">
        <SkeletonLine className="w-40 h-5" />
        <SkeletonLine className="w-20 h-6 rounded-full" />
      </div>
      <div className="mt-2 space-y-2">
        <SkeletonLine className="w-full" />
        <SkeletonLine className="w-11/12" />
        <SkeletonLine className="w-3/4" />
      </div>
      <div className="bg-stone-100 border border-stone-200 rounded-lg p-5 mt-6">
        <div className="flex justify-between items-center mb-3">
          <SkeletonLine className="w-24 h-3" />
          <SkeletonLine className="w-12 h-7 rounded-md" />
        </div>
        <div className="space-y-2">
          <SkeletonLine className="w-full" />
          <SkeletonLine className="w-full" />
          <SkeletonLine className="w-5/6" />
          <SkeletonLine className="w-2/3" />
        </div>
      </div>
    </div>
  )
}
