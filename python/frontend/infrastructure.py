from constructs import Construct
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_wafv2 as wafv2
from aws_cdk import Stack
from aws_cdk import RemovalPolicy

class StaticSiteStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3 bucket for website content
        bucket = s3.Bucket(self, "StaticSiteBucket-arpantech",
            website_index_document="index.html",
            public_read_access=False,
            removal_policy=RemovalPolicy.DESTROY)  # BE CAREFUL with the removal policy

        # OAI for CloudFront
        oai = cloudfront.OriginAccessIdentity(self, "OAI",
            comment="OAI for static site")

        # Grant OAI permissions to read the bucket
        bucket.grant_read(oai)

        # # WAF for CloudFront
        # web_acl = wafv2.CfnWebACL(self, "WebACL",
        #     default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
        #     scope="CLOUDFRONT",
        #     visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
        #         cloud_watch_metrics_enabled=True,
        #         sampled_requests_enabled=True,
        #         metric_name="webACL",
        #     ),
        #     rules=[]  # Add your rules here
        #     )

        # CloudFront distribution
        distribution = cloudfront.CloudFrontWebDistribution(self, "CloudFront",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=bucket,
                        origin_access_identity=oai),
                    behaviors=[cloudfront.Behavior(
                        is_default_behavior=True)]
                )
            ]
        )

        self.distribution_domain_name2 = distribution.distribution_domain_name

    @property
    def distribution_domain_name(self) -> str:
        return self.distribution_domain_name2