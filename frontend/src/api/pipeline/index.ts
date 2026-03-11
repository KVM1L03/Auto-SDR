import { apiClient } from '../client'
import type { PipelineResponse } from './types'

export const runPipeline = async (companyDomain: string): Promise<PipelineResponse> => {
  const { data } = await apiClient.post<PipelineResponse>('/pipeline', {
    company_domain: companyDomain,
  })
  return data
}