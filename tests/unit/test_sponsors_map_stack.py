import aws_cdk as core
import aws_cdk.assertions as assertions

from sponsors_map.sponsors_map_stack import SponsorsMapStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sponsors_map/sponsors_map_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SponsorsMapStack(app, "sponsors-map")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
