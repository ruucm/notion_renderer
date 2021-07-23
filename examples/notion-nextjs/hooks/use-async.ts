import React from "react"
/**
 * A hook to fetch async data. (code from https://stackoverflow.com/questions/56450975/to-fix-cancel-all-subscriptions-and-asynchronous-tasks-in-a-useeffect-cleanup-f)
 * @class useAsync
 * @borrows useAsyncObject
 * @param {object} _                props
 * @param {async} _.asyncFunc         Promise like async function
 * @param {bool} _.immediate=false    Invoke the function immediately
 * @param {object} _.funcParams       Function initial parameters
 * @param {object} _.initialData      Initial data
 * @returns {useAsyncObject}        Async object
 * @example
 *   const { execute, loading, data, error } = useAsync({
 *    asyncFunc: async () => { return 'data' },
 *    immediate: false,
 *    funcParams: { data: '1' },
 *    initialData: 'Hello'
 *  })
 */
export const useAsync = (props: any) => {
  const { asyncFunc, immediate, funcParams, initialData } = props

  const [loading, setLoading] = React.useState(immediate)
  const [data, setData] = React.useState(initialData)
  const [error, setError] = React.useState(null)
  const mountedRef = React.useRef(true)

  const execute = React.useCallback(
    (params) => {
      setLoading(true)
      return asyncFunc({ ...funcParams, ...params })
        .then((res: any) => {
          if (!mountedRef.current) return null
          setData(res)
          setError(null)
          setLoading(false)
          return res
        })
        .catch((err: any) => {
          if (!mountedRef.current) return null
          setError(err)
          setLoading(false)
          throw err
        })
    },
    [asyncFunc, funcParams]
  )

  React.useEffect(() => {
    if (immediate) {
      execute(funcParams)
    }
    return () => {
      mountedRef.current = false
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return {
    execute,
    loading,
    data,
    error,
  }
}
