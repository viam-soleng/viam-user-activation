// Package main is the entrypoint for the viam-user-activation module.
package main

import (
	"go.viam.com/rdk/components/sensor"
	"go.viam.com/rdk/module"
	"go.viam.com/rdk/resource"

	"github.com/viam-soleng/viam-user-activation/models"
)

func main() {
	// ModularMain registers the model(s) this module provides and runs the
	// module until it receives a termination signal.
	module.ModularMain(resource.APIModel{API: sensor.API, Model: models.UserActivation})
}
