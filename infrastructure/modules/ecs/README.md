aws ecs describe-tasks --cluster api-cluster-name --tasks arn:aws:ecs:us-west-2:<account-id>:task/api-cluster/xxxxxxxxxx  | grep -i "eni-"

aws ec2 describe-network-interfaces --network-interface-ids eni-xxxxxxxxx | grep -i "publicip"