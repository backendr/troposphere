#!/usr/bin/env python3

# Copyright (c) 2019 Matthew Lowe
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse

from troposphere import Template, Output, Ref, Tags
from troposphere.ec2 import VPC, InternetGateway, VPCGatewayAttachment, \
    NetworkAcl, NetworkAclEntry, PortRange


def get_args():
    """
    returns parsed command line input via `argparse`.
    """
    parser = argparse.ArgumentParser(description='Generates Service VPC Cloudformation. Default output is JSON.')
    parser.add_argument('env', help='Name of environment')
    parser.add_argument('-y', '--yaml', action='store_true', required=False, help='Output to YAML')
    return parser.parse_args()


if __name__ == '__main__':
    # validate
    args = get_args()

    # create template
    template = Template()
    template.set_version('2010-09-09')
    template.set_description('Service VPC')
    template.set_metadata({
        'DependsOn': [],
        'Environment': args.env,
        'StackName': '{}-VPC'.format(args.env)})
    vpc = template.add_resource(
        VPC('VPC',
            CidrBlock='10.0.0.0/16',
            EnableDnsHostnames=True,
            EnableDnsSupport=True,
            InstanceTenancy='default',
            Tags=Tags(Environment=args.env,
                      Name='{}-ServiceVPC'.format(args.env))
            )
    )
    internet_gateway = template.add_resource(
        InternetGateway('InternetGateway',
                        Tags=Tags(Environment=args.env,
                                  Name='{}-InternetGateway'.format(args.env))
                        )
    )
    template.add_resource(
        VPCGatewayAttachment('VpcGatewayAttachment',
                             InternetGatewayId=Ref(internet_gateway),
                             VpcId=Ref(vpc))
    )
    vpc_network_acl = template.add_resource(
        NetworkAcl('VpcNetworkAcl',
                   VpcId=Ref(vpc),
                   Tags=Tags(Environment=args.env,
                             Name='{}-NetworkAcl'.format(args.env)))
    )
    template.add_resource(
        NetworkAclEntry('VpcNetworkAclInboundRule',
                        CidrBlock='0.0.0.0/0',
                        Egress=False,
                        NetworkAclId=Ref(vpc_network_acl),
                        PortRange=PortRange(From=443, To=443),
                        Protocol=6,
                        RuleAction='allow',
                        RuleNumber=100)
    )
    template.add_resource(
        NetworkAclEntry('VpcNetworkAclOutboundRule',
                        CidrBlock='0.0.0.0/0',
                        Egress=True,
                        NetworkAclId=Ref(vpc_network_acl),
                        Protocol=6,
                        RuleAction='allow',
                        RuleNumber=200)
    )
    template.add_output([
        Output("InternetGateway",
               Description='Resource Name for Service VPC Internet Gateway',
               Value=Ref(internet_gateway)),
        Output("VPCID",
               Description='Resource Id for Service VPC',
               Value=Ref(vpc))
    ])

    # output
    if args.yaml:
        print(template.to_yaml())
    else:
        print(template.to_json())
