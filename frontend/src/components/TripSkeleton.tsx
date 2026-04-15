export function TripSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Summary skeleton */}
      <div className="rounded-xl border p-6 space-y-3">
        <div className="h-5 bg-gray-200 rounded w-1/4" />
        <div className="h-4 bg-gray-200 rounded w-full" />
        <div className="h-4 bg-gray-200 rounded w-5/6" />
        <div className="h-4 bg-gray-200 rounded w-4/5" />
        <div className="h-4 bg-gray-200 rounded w-full" />
        <div className="h-4 bg-gray-200 rounded w-3/4" />
      </div>

      {/* Photos skeleton */}
      <div className="rounded-xl border p-6 space-y-3">
        <div className="h-5 bg-gray-200 rounded w-1/4" />
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-48 bg-gray-200 rounded-lg" />
          ))}
        </div>
      </div>

      {/* Cost + Exchange skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-xl border p-6 space-y-2">
          <div className="h-5 bg-gray-200 rounded w-1/3" />
          <div className="h-7 bg-gray-200 rounded w-1/2" />
          <div className="h-4 bg-gray-200 rounded w-2/3" />
        </div>
        <div className="rounded-xl border p-6 space-y-2">
          <div className="h-5 bg-gray-200 rounded w-1/3" />
          <div className="h-4 bg-gray-200 rounded w-1/2" />
        </div>
      </div>

      {/* Weather skeleton */}
      <div className="rounded-xl border p-6 space-y-3">
        <div className="h-5 bg-gray-200 rounded w-1/4" />
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-24 bg-gray-200 rounded-lg" />
          ))}
        </div>
      </div>
    </div>
  );
}
