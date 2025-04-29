locals {
  BLOSSOM_NIST = {
  
    network_name          = "Blossom"
    network_id            = "n-FLXXKM7INVCDXGQMUAH633E6PQ"

    member_name           = "NIST"
    member_id             = "m-DTLKIKVWWZER3DUHQUDH43I7YQ"

    peer_node_id          = "nd-BURDFKAXHRFD3JHWFTPPPEJJ4M"

//    channel_name          = "blossom1"
//    contract_name         = "blossom"
    channel_name          = "authorization"
    contract_name         = "authorization"
    auth_channel          = "authorization"
    auth_contract         = "authorization"
    bus_channel           = "business"
    bus_contract          = "business"

    identities_ssm_prefix = "/nist/blossom/dev/user"
    cognito_domain_prefix = "blossom_test"
  }
  #   BLOSSOM_NIST_SAM = {

  #   network_name            = "BlossomNIST"
  #   network_id              = "n-Q3IXPKVC7FC7XL2XMUWKRMQ7T4"

  #   member_name             = "SAM-NIST-TF"
  #   member_id               = "m-6YQE3YRQTFBB3MT7V32ZZWA7QA"

  #   peer_node_id            = "nd-BCKHS3NJO5H3LGTZNUOMJ3NDOQ"

  #   channel_name           = "blossom-auth"
  #   contract_name           = "blossom-auth-cc"
  #   auth_channel            = "blossom-auth"
  #   auth_contract           = "blossom-auth-cc"
  #   bus_channel             = "blossom-asset"
  #   bus_contract            = "blossom-asset-cc"
    
    
  #   identities_ssm_prefix   = "/nist/blossom/dev/user"
  #   cognito_user_pool_name  = "blossom_test"

  #   apigw_s3_integration_iam_role_name = "frontend-apigw-s3-integration-role"
  #   lambda_execution_iam_role_name = "LambdaExecutionRole"
  # }
}
